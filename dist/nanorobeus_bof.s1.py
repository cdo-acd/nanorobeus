from typing import List, Tuple

from outflank_stage1.task.base_bof_task import BaseBOFTask
from outflank_stage1.task.enums import BOFArgumentEncoding


class NanorobeusBOF(BaseBOFTask):
    def __init__(self):
        super().__init__("nanorobeus")

        _command_choices = ["luid", "sessions", "klist", "dump", "ptt", "purge", "tgtdeleg", "kerberoast"]

        self.parser.description = (
            "COFF file (BOF) for managing Kerberos tickets."
        )
        self.parser.epilog = "luid - get current logon ID\n\nsessions [/luid:<0x0>| /all] - get logon sessions\n\nklist [/luid:<0x0> | /all] - list Kerberos tickets\n\ndump [/luid:<0x0> | /all] - dump Kerberos tickets\n\nptt /ticket:<base64> [/luid:<0x0>] - import Kerberos ticket into a logon session\n\npurge [/luid:<0x0>] - purge Kerberos tickets\n\ntgtdeleg /spn:<spn> - retrieve a usable TGT for the current user\n\nkerberoast /spn:<spn> - perform Kerberoasting against specified SPN"

        self.parser.add_argument(
            "command",
            choices=_command_choices,
            help=f"Commands ({', '.join(_command_choices)}).",
            metavar="command",
        )

        self.parser.add_argument(
            "arguments",
            help="Arguments for commands",
            nargs="*",
        )

    def _encode_arguments_bof(
        self, arguments: List[str]
    ) -> List[Tuple[BOFArgumentEncoding, str]]:
        parser_arguments = self.parser.parse_args(arguments)

        if parser_arguments.arguments:
            split_arguments = self.split_arguments(parser_arguments.arguments)
            returnList = [(BOFArgumentEncoding.STR, parser_arguments.command)]
            for argument in split_arguments:
                returnList.append((BOFArgumentEncoding.STR, argument))
            return returnList

        else:
            return [(BOFArgumentEncoding.STR, parser_arguments.command)]
