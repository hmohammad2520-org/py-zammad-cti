from classmods import ENVMod
from zammad_cti import CTIClient as _


def test_create_env():
    ENVMod.save_example()
    ENVMod.sync_env_file()
