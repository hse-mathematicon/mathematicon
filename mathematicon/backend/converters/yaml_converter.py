import os
import re
from pathlib import Path
from typing import Iterable, Union, Callable, Dict, Any

import yaml
import spacy
from spacy import Language
from spacy_conll import ConllParser
from yaml.parser import ParserError

from ..models.db_data_models import DatabaseText
from ..models.database import TextDBHandler


class YamlConverter:
    def __init__(self,
                 filepaths: Iterable[Union[str, os.PathLike]],
                 text_preprocess: Callable[[str], str] = None):
        if not text_preprocess:
            text_preprocess = self._remove_double_spaces
        self.yaml_contents = self._load_yamls(filepaths, text_preprocess)

    @staticmethod
    def _remove_double_spaces(text: str) -> str:
        return re.sub(r"\s+", " ", text)

    @staticmethod
    def _load_yamls(filepaths: Iterable[Union[str, os.PathLike]],
                    preprocess: Callable[[str], str]) -> Dict[Path, Dict[str, Any]]:
        """
        Read texts that are stored in yaml files
        Args:
            filepaths: iterable of paths to yaml files
            preprocess: callable that preprocesses text field from the yaml file

        Returns: {filepath: {field: values}}

        """
        files_info = {}
        for p in filepaths:
            p = Path(p).resolve()
            with open(p, encoding='utf-8') as f:
                try:
                    read_data = yaml.load(f, Loader=yaml.FullLoader)
                    read_data["text"] = preprocess(read_data["text"])
                    files_info[p] = read_data
                except ParserError as e:
                    print(e)
                    print()
                    print(f'Some problems with file {f}')
                finally:
                    continue
        return files_info

    def to_conllu(self,
                  nlp: Language,
                  dest_folder: Union[str, os.PathLike]) -> Iterable[Path]:
        dest_folder = Path(dest_folder).resolve()
        dest_folder.mkdir(parents=True, exist_ok=True)

        if 'conllu_formatter' not in [pipe[0] for pipe in nlp.pipeline]:
            nlp.add_pipe("conll_formatter", last=True, config={'include_headers': True})

        written_files = []
        for file, info in self.yaml_contents.items():
            doc = nlp(info['text'])
            result_path = Path(dest_folder, file.with_suffix(".conllu").name)
            with open(result_path, "w", encoding="utf-8") as f:
                f.write(doc._.conll_str)
            written_files.append(result_path)
        return written_files

    def to_database(self,
                    nlp: Language,
                    db: TextDBHandler):
        for file, info in self.yaml_contents.items():
            db_text_info = {k: v for k, v in info.items() if k not in ['text']}
            doc = nlp(info['text'])
            db_text = DatabaseText(doc, filename=file.stem, **db_text_info)
            db.add_text(db_text)
            for sent in db_text:
                db.add_sentence(sent)
                db.add_sentence_tokens(sent)


def update_ud_annot(conllu_file: Union[str, os.PathLike],
                    db: TextDBHandler,
                    nlp: Language):
    conllu_file = Path(conllu_file).resolve()
    filename = conllu_file.stem
    if 'conllu_formatter' not in [pipe[0] for pipe in nlp.pipeline]:
        nlp.add_pipe("conll_formatter", last=True, config={'include_headers': True})
    conllu_nlp = ConllParser(nlp)
    conllu_doc = conllu_nlp.parse_conll_file_as_spacy(conllu_file)
    for sent in DatabaseText(conllu_doc, filename=filename):
        db.update_sentence_grammar_annotation(sent)


if __name__ == '__main__':
    from mathematicon import DB_PATH
    from mathematicon.backend.models.mathematicon_morph_parser import MorphologyCorrectionHandler
    from spacy.language import Language

    db = TextDBHandler(DB_PATH)

    @Language.factory(
        "morphology_corrector",
        assigns=["token.lemma", "token.tag"],
        requires=["token.pos"],
        default_config={"mode": "ptcp+conv"},
    )
    def morphology_corrector(nlp, name, mode):
        return MorphologyCorrectionHandler(mode=mode)
    nlp = spacy.load("ru_core_news_sm", exclude=["ner"])
    nlp.add_pipe('morphology_corrector', after='lemmatizer')

    mode = input('Enter mode (parse or update): ')
    if mode == 'parse':
        files = input("Directory with files or filepaths: ").split(" ")
        if len(files) < 2 and Path(files[0]).is_dir():
            files = [x for x in Path(files[0]).iterdir() if x.suffix == '.txt']
        yaml_converter = YamlConverter(files)

        dest = input('Select destination (conllu or database): ')

        if dest == 'database':
            yaml_converter.to_database(nlp, db)
        elif dest == 'conllu':
            dest_folder = input('Path to destination folder: ')
            yaml_converter.to_conllu(nlp, dest_folder)
    elif mode == 'update':
        conllu_file = input('Path to conllu: ')
        update_ud_annot(conllu_file, db, nlp)