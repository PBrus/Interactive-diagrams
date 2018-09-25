from matplotlib import pyplot as plt
from matplotlib.widgets import Button
from idgrms.data import (list_iterator, get_specific_data, get_marked_points,
    get_colored_points, mark_points, feedback)


marked_data_indexes = None

def get_figures(columns_argument, talk_argument, all_data):
    figures = ()
    global marked_data_indexes

    for _ in list_iterator(columns_argument):
        figure = plt.figure()
        axis = figure.add_subplot(111)
        plt.subplots_adjust(bottom=0.15)
        axis.save = plt.axes([0.125, 0.05, 0.15, 0.05])
        axis.save_button = Button(axis.save, 'Snapshot')
        axis.save_button.on_clicked(lambda event: save_img())

        if not talk_argument:
            axis.info = plt.axes([0.75, 0.05, 0.15, 0.05])
            axis.info_button = Button(axis.info, 'Feedback')
            axis.info_button.on_clicked(
                lambda event: feedback(all_data, marked_data_indexes))

        figures += figure,

    return figures

def draw_all_figures(figures, data, columns_argument, groups_argument,
                     marked_data=(), colored_data=()):

    for figure, columns in zip(figures, columns_argument):
        points, axes_labels, axes_orientation = (
            get_specific_data(data, columns))
        marked_points = get_marked_points(data, marked_data, columns)
        colored_points = get_colored_points(data, colored_data, columns,
                                            groups_argument)
        # Clean a figure.
        figure.axes[0].cla()
        set_axes_labels(figure, axes_labels, len(data[-1][-1]))
        set_axes_orientation(figure, axes_orientation)

        plot_diagram(figure, points, marked_points, colored_points)

def set_axes_labels(figure, axes_labels, points_number):
    figure.axes[0].set_title("Diagram for " + str(points_number) + " points",
                             fontsize=20)
    figure.axes[0].set_xlabel(axes_labels[0], fontsize=15)
    figure.axes[0].set_ylabel(axes_labels[1], fontsize=15)

def set_axes_orientation(figure, axes_orientation):
    if axes_orientation[0] < 0:
        figure.axes[0].invert_xaxis()
    if axes_orientation[1] < 0:
        figure.axes[0].invert_yaxis()

def plot_diagram(figure, points=(), marked_points=(), colored_points=()):
    # Redefined to be more readable.
    ax = figure.axes[0]
    ax.scatter(points[0], points[1], 60, c='gray', alpha=0.4, zorder=1)

    if marked_points != ():
        ax.scatter(marked_points[0], marked_points[1], 100, c='red',
                   alpha=1.0, zorder=3)
    if colored_points != ():
        for cp in colored_points:
            ax.scatter(cp[0], cp[1], 60, c=cp[2], alpha=0.6, zorder=2)

    ax.scatter(points[0], points[1], 50, alpha=0.0, picker=3)
    figure.canvas.draw_idle()

def connect_figures(figures, all_data, data,
                    columns_argument, groups_argument, talk_argument,
                    marked_data=(), colored_data=()):

    def pick_point(event):
        global marked_data_indexes
        marked_data_indexes = event.ind
        marked_data = mark_points(data, marked_data_indexes)
        draw_all_figures(figures, data, columns_argument, groups_argument,
                         marked_data, colored_data)

        if talk_argument:
            feedback(all_data, marked_data_indexes)

    for figure in figures:
        figure.canvas.mpl_connect('pick_event', pick_point)
