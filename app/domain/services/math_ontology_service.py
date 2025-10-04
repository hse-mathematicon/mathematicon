from dataclasses import dataclass
from typing import BinaryIO, Optional

from bs4 import BeautifulSoup
from bs4.element import Tag
from loguru import logger

from app.domain.entities.math_ontology import MathTagAttributeModel, MathTagModel
from app.domain.services.interfaces.math_ontology import MathOntologyInterface
from app.settings.rdf import RDFSettings


@dataclass
class MathOntologyService:
    _rdf_settings: RDFSettings
    _ontology_adapter: MathOntologyInterface

    def load_from_rdf(self, file_content: BinaryIO) -> None:
        tags = []
        soup = BeautifulSoup(file_content, features="xml")
        for el in soup.find_all(self._is_math_tag_element):
            try:
                tags.append(self._get_tag_info_from_xml_element(el))
            except Exception as e:
                logger.error(f"Failed to process {el}. Exception: {e}")
        self._ontology_adapter.put_math_ontology(tags)

    def _is_math_tag_element(self, tag: Tag) -> bool:
        tag_id = tag.attrs.get("rdf:about", "")
        return (
            tag.name == "Description"
            and isinstance(tag_id, str)
            and tag_id.startswith(self._rdf_settings.base_prefix)
        )

    def _get_tag_info_from_xml_element(self, element: Tag) -> MathTagModel:
        inception_id = str(element["rdf:about"]).removeprefix(
            self._rdf_settings.base_prefix
        )
        parent_id = self._get_parent_id(element)
        attrs = self._get_tag_attrs_from_xml_element(element, inception_id)
        return MathTagModel(inception_id=inception_id, parent_id=parent_id, attrs=attrs)

    def _get_parent_id(self, element: Tag) -> Optional[str]:
        for tag in element.find_all(self._rdf_settings.parent_tags):
            resource = tag.get("rdf:resource")
            if resource and str(resource).startswith(self._rdf_settings.base_prefix):
                return str(resource).removeprefix(self._rdf_settings.base_prefix)
        return None

    def _get_tag_attrs_from_xml_element(
        self, element: Tag, math_tag_id: str
    ) -> list[MathTagAttributeModel]:
        attrs = []
        for tag in element.find_all(self._rdf_settings.tag_attr_keys):
            try:
                attrs.append(
                    MathTagAttributeModel(
                        math_tag_id=math_tag_id,
                        key=tag.name,
                        language=str(tag.get("xml:lang")),
                        value=tag.get_text(strip=True),
                    )
                )
            except Exception as e:
                logger.error(f"Invalid attribute for {math_tag_id}: {e}")
        return attrs
