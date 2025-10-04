from pathlib import Path

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton
from dotenv import load_dotenv
from sqlalchemy.engine import Engine

from app.domain.services.grammar_annotation_service import GrammarAnnotationService
from app.domain.services.interfaces.language_parser import LanguageParserInterface
from app.infra.adapters import SentencesAdapter, SpacyLanguageParser, TranscriptsAdapter
from app.infra.db.engine import get_engine
from app.settings import DBSettings, ServerSettings
from app.variables import PROJECT_DIR

load_dotenv(Path(PROJECT_DIR, ".env"))


class AppContainer(DeclarativeContainer):
    """Контейнер с зависимостями."""

    # Settings
    server_settings: Singleton[ServerSettings] = Singleton(ServerSettings)
    db_settings: Singleton[DBSettings] = Singleton(DBSettings)

    # Database
    engine: Singleton[Engine] = Singleton(get_engine, db_settings=db_settings.provided)

    # Storage adapters
    transcripts_adapter: Factory[TranscriptsAdapter] = Factory(
        TranscriptsAdapter, _db_engine=engine.provided
    )
    sentences_adapter: Factory[SentencesAdapter] = Factory(
        SentencesAdapter, _db_engine=engine
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
