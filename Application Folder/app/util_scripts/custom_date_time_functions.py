


def import_non_local(name, custom_name=None):
    import imp, sys

    custom_name = custom_name or name

    f, pathname, desc = imp.find_module(name, sys.path[1:])
    module = imp.load_module(custom_name, f, pathname, desc)
    f.close()

    return module


datetime_main = import_non_local('datetime','std_datetime')


def get_past_date(no_of_days):
	return datetime_main.date.today()-datetime_main.timedelta(no_of_days)