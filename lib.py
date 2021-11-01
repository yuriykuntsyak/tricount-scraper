import re
import pydantic


class Expense(pydantic.BaseModel):
    description: str
    amount: str
    date: str
    payer_name: str
    paid_for_user: str
    state: str

    @pydantic.validator("date")
    @classmethod
    def date_validator(cls, value):
        validation_errors: str = ""

        if len(value) < len("1/1/1"):
            validation_errors += "Invalid date length. "

        re_match = re.fullmatch(
            pattern=r"^(?P<dd>[0-9]+)\/(?P<mm>[0-9]+)\/(?P<yy>[0-9]+)$", string=value
        )
        if re_match:
            date_dict = re_match.groupdict()

            if not (
                1 <= int(date_dict["dd"]) <= 31
                and 1 <= int(date_dict["mm"]) <= 12
                and int(date_dict["yy"]) > 0
            ):
                validation_errors += "Invalid value of day, month or year. "
        else:
            validation_errors += "Invalid date format. "

        if validation_errors:
            raise ValueError(validation_errors + "Expected DD/MM/YY, got:" + repr(value))

        return (
            value.split("/")[0].zfill(2)
            + "/"
            + value.split("/")[1].zfill(2)
            + "/"
            + value.split("/")[2][-2:].zfill(2)
        )
