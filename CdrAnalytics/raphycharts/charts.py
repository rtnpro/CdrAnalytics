import json
import copy

class RaphyChart(object):
    type = "generic"

    def __init__(self, data=[], style_options={}, chart_id="raphy-chart"):
        self.data = data
        self.style_options = style_options
        self.chart_id = chart_id


class RaphyLineChart(RaphyChart):
    
    def __init__(self, data=[], style_options={}, x_axis_type='numeric',
        y_axis_type='numeric'):
        super(RaphyLineChart, self).__init__(data, style_options)
        self.style = "linechart"
        self.x_axis_type = x_axis_type
        self.y_axis_type = y_axis_type

    def process_date(self,  date):
        return {
            'year': date.year,
            'month': date.month - 1,
            'day': date.day,
            'hour': date.hour,
            'minute': date.minute,
            'second': date.second
        }

    def visit_point_x(self, x):
        if self.x_axis_type == 'date':
            return self.process_date(x)
        return x

    def visit_point_y(self, y):
        if self.y_axis_type == 'date':
            return self.process_date(y)
        return y

    def create_tooltip(self, point):
        print point
        return "%s at %s" % (point[0], point[1])

    def visit_point(self, point):
        return [self.visit_point_x(point[0]), self.visit_point_y(point[1]),
            self.create_tooltip(point)]

    def get_plot_data(self):
        data = copy.copy(self.data)
        for n, point in enumerate(data):
            data[n] = self.visit_point(point)
        return data

    def get_plot_options(self):
        return self.style_options

    def get_json_for_plot(self):
        return json.dumps({
            'plot': self.get_plot_data(),
            'options': self.get_plot_data()
            })