from matplotlib import pyplot as plt
from matplotlib.widgets import Button
from idgrms.data import get_specific_data


def get_figures(columns_argument, talk_argument):
    figures = ()

    for _ in columns_amount_iterator(columns_argument):
        figure = plt.figure()
        axis = figure.add_subplot(111)
        axis.save = plt.axes([0.125, 0.05, 0.15, 0.05])
        axis.save_button = Button(axis.save, 'Snapshot')
        axis.save_button.on_clicked(lambda event: save_img())

        if talk_argument != None:
            axis.info = plt.axes([0.75, 0.05, 0.15, 0.05])
            axis.info_button = Button(axis.info, 'Feedback')
            axis.info_button.on_clicked(lambda event: feedback(idevnt))

        figures += figure,

    return figures

def columns_amount_iterator(columns_argument):
    return range(len(columns_argument))

def draw_all_figures(figures, data, columns_argument,
                     marked_data=(), colored_data=()):

    mkd = ()
    cld = ()

    for figure, columns in zip(figures, columns_argument):
        points_position, axes_labels, axes_orientation = (
            get_specific_data(data, columns))
        plot_diagram(figure, figure.axes[0], axes_orientation,
                     axes_labels, points_position, mkd, cld)
