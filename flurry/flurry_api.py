import time
import requests
try:
    import urlparse
except:     # For Python 3
    import urllib.parse as urlparse

from flurry.utils import stringify_list


tables = {
    "appUsage": {
        "time_grain": ['day', 'week', 'month', 'all'],
        "dimensions": ["company", "app", "appVersion", "country", "language", "region", "category"],
        "metrics": ["sessions", "activeDevices", "newDevices", "timeSpent", "averageTimePerDevice", "averageTimePerSession"]
    },
    "appEvent": {
        "time_grain": ['day', 'week', 'month', 'all'],
        "dimensions": ["company", "app", "appVersion", "country", "language", "region", "category", "event", "paramName", "paramValue"],
        "metrics": ["activeDevices", "newDevices", "timeSpent", "averageTimePerDevice", "averageTimePerSession", "occurrences"]
    },
    "realtime": {
        "time_grain": ['hour', 'day', 'all'],
        "dimensions": ["company", "app", "appVersion", "country"],
        "metrics": ["sessions", "activeDevices"]
    }
}


class Flurry_api(object):
    def __init__(self, start, end, flurry_token):
        """
        Format for Day, Week: YYYY-MM-DD
        Format for Month    : YYYY-MM
        Format for Hour     : YYYY-MM-DDTHH
        """
        self.start_date = start
        self.end_date = end
        self.headers = {'Authorization': 'Bearer ' + flurry_token}
        self.base_url = "https://api-metrics.flurry.com/public/v1/data/"
        # self.events_api_url = urlparse.urljoin(base_url, "realtime")

    def get_app_metric(self, table, time_grain, dimensions, metrics, filter_country_iso=[]):
        """
        app_metric must be one of the following:
        ActiveUsers, NewUsers, MedianSessionLength, AvgSessionLength,
        Sessions, RetainedUsers, PageViews, AvgPageViewsPerSession

        For more information, please see:
        https://developer.yahoo.com/flurry/docs/api/code/appmetrics/

        """
        choice_tables = tables.keys()
        if table not in choice_tables:
            str_choice_tables = stringify_list(choice_tables)
            print("""{0} is not a valid table.\n\nPlease choose 1 or more of the following:\n{1}
            """).format(table, str_choice_tables)
        else:
            choice_time_grain = tables[table]["time_grain"]
            choice_dimensions = tables[table]["dimensions"]
            choice_metrics = tables[table]["metrics"]
            if time_grain not in choice_time_grain:
                str_choice_time_grain = stringify_list(choice_time_grain)
                print """{0} is not a valid time grain for {1}.\n\nPlease choose 1 or more of the following:\n{2}
                """.format(time_grain, table, str_choice_time_grain)
            elif not(set(dimensions) < set(choice_dimensions)):
                str_choice_dimensions = stringify_list(choice_dimensions)
                print """{0} is not a valid dimension for {1}.\n\nPlease choose 1 or more of the following:\n{2}
                """.format(stringify_list(dimensions), table, str_choice_dimensions)
            elif not(set(metrics) < set(choice_metrics)):
                str_choice_metrics = stringify_list(choice_metrics)
                print """{0} is not a valid metric for {1}.\n\nPlease choose 1 or more of the following:\n{2}
                """.format(stringify_list(metrics), table, str_choice_metrics)
            else:
                # API url construction and query
                dimensions_chosen = [dimension for dimension in choice_dimensions if dimension in dimensions]
                params = [table, time_grain] + dimensions_chosen
                get_url = self.base_url
                for param in params:
                    get_url = urlparse.urljoin(get_url, param + "/")
                get_url = get_url[:-1]

                str_metrics_chosen = stringify_list([metric for metric in choice_metrics if metric in metrics]).replace(" ", "")
                get_url = get_url + "?metrics=" + str_metrics_chosen + "&dateTime=" + self.start_date + "/" + self.end_date

                if filter_country_iso:
                    get_url = get_url + "&filters=country|iso-in" + str(filter_country_iso).replace(" ", "").replace("'", "").upper()

                print "API url:\n{}\n".format(get_url)
                time.sleep(1)
                response = requests.get(get_url, headers=self.headers)

                if response.status_code == 200:
                    results = response.json()
                    return results["rows"]
                else:
                    print "Response failed with status: {}".format(response.status_code)
                    print "Error description: {}".format(response.json()["description"])
