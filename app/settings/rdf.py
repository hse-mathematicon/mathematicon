from pydantic_settings import BaseSettings, SettingsConfigDict


class RDFSettings(BaseSettings):
    base_prefix: str = "http://www.ukp.informatik.tu-darmstadt.de/inception/1.0#"
    tag_attr_keys: list[str] = ["label", "comment"]
    parent_tags: list[str] = ["subClassOf", "rdf:type"]

    model_config = SettingsConfigDict(env_prefix="rdf_")
