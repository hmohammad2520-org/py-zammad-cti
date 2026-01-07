from typing import TypeAlias, Literal

CallDirection: TypeAlias = Literal['in', 'out']
HangupCause: TypeAlias = Literal[
    'normalClearing',
    'busy',
    'cancel',
    'noAnswer',
    'congestion',
    'notFound',
    'forwarded',
]
