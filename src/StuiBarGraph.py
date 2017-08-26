from ComplexBarGraphs import LabeledBarGraph
from ComplexBarGraphs import ScalableBarGraph
import logging
logger = logging.getLogger(__name__)

class StuiBarGraph(LabeledBarGraph):

    @staticmethod
    def append_latest_value(values, new_val):

        values.append(new_val)
        return values[1:]

    MAX_SAMPLES = 1000
    SCALE_DENSITY = 5

    def __init__(self, source, color_a, color_b, smooth_a, smooth_b, bar_width = 1):
        self.source = source
        self.graph_name = self.source.get_source_name()
        self.measurement_unit = self.source.get_measurement_unit()

        self.num_samples = self.MAX_SAMPLES
        self.graph_data = [0] * self.num_samples

        self.color_a = color_a
        self.color_b = color_b
        self.smooth_a = smooth_a
        self.smooth_b = smooth_b


        x_label = []
        y_label = []

        w = ScalableBarGraph(['bg background', color_a, color_b])
        super(StuiBarGraph, self).__init__([w, x_label, y_label, self.graph_name + ' [' + self.measurement_unit + ']'])
        self.bar_graph.set_bar_width(bar_width)


    def get_current_summary(self):
        pass

    def get_graph_name(self):
        return self.graph_name

    def get_measurement_unit(self):
        return self.measurement_unit

    def get_is_available(self):
        return self.source.get_is_available()

    def get_label_scale(self, min_val, max_val, size):
        """Dynamically change the scale of the graph (y lable)"""
        if size < self.SCALE_DENSITY:
            label_cnt = 1
        else:
            label_cnt = (size / self.SCALE_DENSITY)
        try:
            label = [int(min_val + i * (int(max_val) - int(min_val)) / label_cnt)
                     for i in range(label_cnt + 1)]
            return label
        except:
            return ""

    def set_smooth_colors(self, smooth):
        satt = None
        if smooth:
            satt = {(1, 0): self.smooth_a, (2, 0): self.smooth_b}
        self.bar_graph.set_segment_attributes(['bg background', self.color_a, self.color_b], satt=satt)


    def update_displayed_graph_data(self):
        if not self.get_is_available():
            return

        l = []

        current_reading = self.source.get_reading()
        logging.info("Reading " + str(current_reading))
        data_max = self.source.get_maximum()
        self.graph_data = self.append_latest_value(self.graph_data, current_reading)

        # Get the graph width (dimension 1)
        num_displayed_bars = self.bar_graph.get_size()[1]
        # print num_displayed_bars
        # Iterage over all the information in the graph
        for n in range(self.MAX_SAMPLES-num_displayed_bars,self.MAX_SAMPLES):
            value = self.graph_data[n]
            # toggle between two bar types
            if n & 1:
                l.append([0, value])
            else:
                l.append([value, 0])

        self.bar_graph.set_data(l, data_max)
        y_label_size = self.bar_graph.get_size()[0]
        s = self.get_label_scale(0, data_max, y_label_size)
        self.set_y_label(s)

    def reset(self):
        self.graph_data = [0] * self.num_samples


    def get_summary(self):
        pass