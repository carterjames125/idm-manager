#!/usr/bin/python3
from dataclasses import dataclass, field
from src.logger import idm_logger
import pathlib
import python_freeipa
import python_freeipa.exceptions
import yaml

@dataclass(kw_only=True, slots=True)
class IdMArchive:
    logger = idm_logger('idm_archive')
    client: python_freeipa.ClientMeta
    dest: pathlib.Path
    limit: int = field(default=1000)

    def create_user_archive(self) -> list:
        self.logger.info("-----------------------------------")
        self.logger.info("CREATING USER OBJECT ARCHIVE")
        self.logger.info("-----------------------------------")
        return list(user for user in self.client.user_find(sizelimit=self.limit)['result'])