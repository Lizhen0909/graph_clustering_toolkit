from gct.dataset import snap_dataset


def list_datasets():
    return snap_dataset.list_datasets()


def get_dataset(name):
    return snap_dataset.get_dataset(name)