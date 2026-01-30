import random, time
from classmods import ENVMod
from zammad_cti import CTIClient

ENVMod.load_dotenv()

client = CTIClient(**ENVMod.load_args(CTIClient.__init__))

def test_simulate_call():
    call_id = str(random.randint(0, 100_000_000))
    _from = '09123456789'
    to = '02145885'
    direction = 'in'
    queue = 'support'
    user = 'admin'
    client.new_call(
        call_id=call_id,
        _from=_from,
        to=to,
        direction=direction,
        queue=queue,
    )
    time.sleep(4)


    client.answer(
        _from=_from,
        to=to,
        direction=direction,
        user=user,
        call_id=call_id,
    )
    time.sleep(10)


    client.hangup(
        call_id=call_id,
        cause='normalClearing',
        _from=_from,
        to=to,
        direction=direction,
    )