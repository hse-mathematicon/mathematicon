from pathlib import Path

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton
from dotenv import load_dotenv
from sqlalchemy.engine import Engine

from app.domain.services.grammar_annotation_service import GrammarAnnotationService
from app.domain.services.interfaces.language_parser import LanguageParserInterface
from app.domain.services.math_annotation_service import MathAnnotationService
from app.domain.services.math_ontology_service import MathOntologyService
from app.domain.services.math_tag_search import MathTagSearchService
from app.infra.adapters import (
    MathAnnotationAdapter,
    MathOntologyAdapter,
    SentencesAdapter,
    SpacyLanguageParser,
    TranscriptsAdapter,
)
from app.infra.db.engine import get_engine
from app.settings import DBSettings, RDFSettings, ServerSettings
from app.variables import PROJECT_DIR

load_dotenv(Path(PROJECT_DIR, ".env"))


class AppContainer(DeclarativeContainer):
    """Контейнер с зависимостями."""

    # Settings
    server_settings: Singleton[ServerSettings] = Singleton(ServerSettings)
    db_settings: Singleton[DBSettings] = Singleton(DBSettings)
    rdf_settings: Singleton[RDFSettings] = Singleton(RDFSettings)

    # Database
    engine: Singleton[Engine] = Singleton(get_engine, db_settings=db_settings.provided)

    # Storage adapters
    transcripts_adapter: Factory[TranscriptsAdapter] = Factory(
        TranscriptsAdapter, _db_engine=engine.provided
    )
    sentences_adapter: Factory[SentencesAdapter] = Factory(
        SentencesAdapter, _db_engine=engine.provided
    )
    math_ontology_adapter: Factory[MathOntologyAdapter] = Factory(
        MathOntologyAdapter, _db_engine=engine.provided
    )
    math_annotation_adapter: Factory[MathAnnotationAdapter] = Factory(
        MathAnnotationAdapter, _db_engine=engine.provided
    )

    # Other adapters
    language_parser: Factory[LanguageParserInterface] = Factory(
        SpacyLanguageParser, "ru_core_news_sm"
    )

    # Services
    grammar_annotation_service: Factory[GrammarAnnotationService] = Factory(
        GrammarAnnotationService,
        _language_parser=language_parser.provided,
        _transcripts_adapter=transcripts_adapter.provided,
        _sentences_adapter=sentences_adapter.provided,
    )
    math_ontology_service: Factory[MathOntologyService] = Factory(
        MathOntologyService,
        _rdf_settings=rdf_settings.provided,
        _ontology_adapter=math_ontology_adapter.provided,
    )
    math_annotation_service: Factory[MathAnnotationService] = Factory(
        MathAnnotationService,
        _sentences_adapter=sentences_adapter.provided,
        _math_annotation_adapter=math_annotation_adapter.provided,
        _inception_tag_prefix=rdf_settings.provided.base_prefix,
    )
    math_tag_search_service: Factory[MathTagSearchService] = Factory(
        MathTagSearchService,
        _transcripts_adapter=transcripts_adapter.provided,
        _sentences_adapter=sentences_adapter.provided,
        _ontology_adapter=math_ontology_adapter.provided,
        _math_annotation_adapter=math_annotation_adapter.provided,
    )
