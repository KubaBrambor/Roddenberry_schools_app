type BasicValue = str | int | float | bool | None
type SimpleDict = dict[str, BasicValue]
type SchoolDict = dict[
    str, BasicValue | SimpleDict | list[SimpleDict] | dict[str, BasicValue | SimpleDict]
]
type APIResponse = dict[str, str | list[SchoolDict] | dict[str, str]]
