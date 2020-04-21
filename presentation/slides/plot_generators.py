import pandas as pd 
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.layouts import gridplot
import os


def errorbar(p, x, y, yerr, source, glyph='circle', glyph_kwargs=None, line_kwargs=None):
        glyph_kwargs = glyph_kwargs or {}
        line_kwargs = line_kwargs or {}
        
        getattr(p, glyph)(x, y, source=source, **glyph_kwargs)
        p.line(x, y, source=source, **line_kwargs)

        error_data = {
            'xbar': [],
            'ybar': [],
        }

        for X, Y, YERR in source[[x, y, yerr]].values:
            error_data['xbar'].append((X, X))
            error_data['ybar'].append((Y - YERR, Y + YERR))

        cds = ColumnDataSource(data=error_data)

        p.multi_line('xbar', 'ybar', source=cds, **line_kwargs)


def od_plot_generator():
    p = figure(plot_width=600, plot_height=450)

    df_0 = pd.read_excel(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'OD600_agg_values.xls'), sheet_name='0uM_agg')
    df_30 = pd.read_excel(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'OD600_agg_values.xls'), sheet_name='30uM_agg')
    df_40 = pd.read_excel(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'OD600_agg_values.xls'), sheet_name='40uM_agg')

    errorbar(p, 'Time', 'mean', 'sem', df_0, glyph='circle',
            glyph_kwargs={'color': 'blue', 'size': 12, 'legend_label': '0uM', 'fill_alpha': 0, 'line_width': 3, 'name': '0'},
            line_kwargs={'color': 'blue', 'line_width': 3, 'legend_label': '0uM'})
    errorbar(p, 'Time', 'mean', 'sem', df_30, glyph='square',
            glyph_kwargs={'color': 'orange', 'size': 12, 'legend_label': '30uM', 'fill_alpha': 0, 'line_width': 3, 'name': '30'},
            line_kwargs={'color': 'orange', 'line_width': 3, 'legend_label': '30uM'})
    errorbar(p, 'Time', 'mean', 'sem', df_40, glyph='triangle',
            glyph_kwargs={'color': 'green', 'size': 12, 'legend_label': '40uM', 'fill_alpha': 0, 'line_width': 3, 'name': '40'},
            line_kwargs={'color': 'green', 'line_width': 3, 'legend_label': '40uM'})

    hover = HoverTool(names=['0', '30', '40'])

    hover.tooltips = [
        ('Ag Conc.', '@ag_conc{uM}'),
        ('Mean', '@mean{0.000}'),
        ('S.E.M.', '@sem{0.000}'),
        ('Count', '@count'),
    ]

    p.add_tools(hover)

    p.xaxis.axis_label = 'Time (hr)'
    p.yaxis.axis_label = 'OD600'
    p.xaxis.axis_label_text_font_size = "20pt"
    p.yaxis.axis_label_text_font_size = "20pt"
    p.xaxis.major_label_text_font_size = "20pt"
    p.xaxis.axis_label_text_font = "times"
    p.xaxis.axis_label_text_font_style = 'normal'
    p.yaxis.major_label_text_font_size = "20pt"
    p.yaxis.axis_label_text_font = "times"
    p.yaxis.axis_label_text_font_style = 'normal'
    p.xaxis.ticker = [-1, 0, 1, 2, 4, 8]

    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    p.legend.label_text_font_size = '20pt'

    return p


def velocity_hists_generator():
    mean_velocities_df = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'mean_velocities_df.csv'), header=None, names=['conc', 'hour', 'mean'])
    sem_velocities_df = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'sem_velocities_df.csv'), header=None, names=['conc', 'hour', 'sem'])
    freq_mean_df = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'freq_mean_df.csv'), header=0)
    freq_sem_df = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'freq_sem_df.csv'), header=0)
    
    freq_mean_df_melted = pd.melt(freq_mean_df, id_vars=['conc', 'hour'], var_name='velocity', value_name='mean')
    freq_sem_df_melted = pd.melt(freq_sem_df, id_vars=['conc', 'hour'], var_name='velocity', value_name='sem')

    freq_df = freq_mean_df_melted
    freq_df['sem'] = freq_sem_df_melted['sem']
    freq_df['sem'] = freq_df['sem'].astype(float)
    freq_df['mean'] = freq_df['mean'].astype(float)
    freq_df['velocity'] = freq_df['velocity'].astype(float)

    means_df = mean_velocities_df
    means_df['sem'] = sem_velocities_df['sem']

    print(freq_df.velocity.dtype)

    p0 = figure(plot_width=400, plot_height=250, x_range=[-0.1, freq_df.velocity.max()*1.05], y_range=[-0.05, 1.4], title='Hour 0')
    p1 = figure(plot_width=400, plot_height=250, x_range=[-0.1, freq_df.velocity.max()*1.05], y_range=[-0.05, 1.4], title='Hour 1')
    p2 = figure(plot_width=400, plot_height=250, x_range=[-0.1, freq_df.velocity.max()*1.05], y_range=[-0.05, 1.4], title='Hour 2')
    p4 = figure(plot_width=400, plot_height=250, x_range=[-0.1, freq_df.velocity.max()*1.05], y_range=[-0.05, 1.4], title='Hour 4')
    p8 = figure(plot_width=400, plot_height=250, x_range=[-0.1, freq_df.velocity.max()*1.05], y_range=[-0.05, 1.4], title='Hour 8')
    p_means = figure(plot_width=400, plot_height=250, x_range=[-0.5, 8.5], title='Mean Velocity vs Time')

    kwarg_mapper = {
        '0': {
            'glyph': 'circle',
            'glyph_kwargs': {
                'color': 'blue',
                'size': 12,
                'legend_label': '0uM',
                'fill_alpha': 0,
                'line_width': 3,
                'name': '0'
            },
            'line_kwargs': {
                'color': 'blue',
                'line_width': 3,
                'legend_label': '0uM'
            }
        },
        '30': {
            'glyph': 'square',
            'glyph_kwargs': {
                'color': 'orange',
                'size': 12,
                'legend_label': '30uM',
                'fill_alpha': 0,
                'line_width': 3,
                'name': '30'
            },
            'line_kwargs': {
                'color': 'orange',
                'line_width': 3,
                'legend_label': '30uM'
            }
        },
        '40': {
            'glyph': 'triangle',
            'glyph_kwargs': {
                'color': 'green',
                'size': 12,
                'legend_label': '40uM',
                'fill_alpha': 0,
                'line_width': 3,
                'name': '40'
            },
            'line_kwargs': {
                'color': 'green',
                'line_width': 3,
                'legend_label': '40uM'
            }
        },
    }

    for j in ['0', '30', '40']:
        for i in list('01248'):
            p = eval(f'p{i}')
            source = freq_df.loc[(freq_df.conc==int(j))&(freq_df.hour==int(i))]
            ratio = 1 / source['mean'].max()
            source['mean'] *= ratio
            source['sem'] *= ratio
            errorbar(p, 'velocity', 'mean', 'sem', source, glyph=kwarg_mapper[j]['glyph'],
                     glyph_kwargs=kwarg_mapper[j]['glyph_kwargs'],
                     line_kwargs=kwarg_mapper[j]['line_kwargs'])

        source2 = means_df.loc[means_df.conc==int(j)]
        errorbar(p_means, 'hour', 'mean', 'sem', source2, glyph=kwarg_mapper[j]['glyph'],
                 glyph_kwargs=kwarg_mapper[j]['glyph_kwargs'],
                 line_kwargs=kwarg_mapper[j]['line_kwargs'])

    hover = HoverTool(names=['0', '30', '40'])

    hover.tooltips = [
        ('Velocity', '@velocity{0.000um/s}'),
        ('Mean', '@mean{0.000}'),
        ('S.E.M.', '@sem{0.000}')
    ]

    hover2 = HoverTool(names=['0', '30', '40'])

    hover2.tooltips = [
        ('Hour', '@hour'),
        ('Mean', '@mean{0.000}'),
        ('S.E.M.', '@sem{0.000}')
    ]

    p_means.add_tools(hover2)
    p_means.yaxis.major_label_text_font_size = "12pt"
    p_means.xaxis.major_label_text_font_size = "12pt"
    p_means.legend.location = "top_right"
    p_means.legend.click_policy = "hide"
    p_means.legend.label_text_font_size = '8pt'
    p_means.title.text_font_size = '12pt'
    p_means.xaxis.ticker = [0, 1, 2, 4, 8]
    p_means.yaxis.axis_label_text_font = "times"
    p_means.yaxis.axis_label_text_font_style = 'normal'
    p_means.xaxis.axis_label_text_font = "times"
    p_means.xaxis.axis_label_text_font_style = 'normal'
    p_means.yaxis.axis_label_text_font_size = '12pt'
    p_means.xaxis.axis_label_text_font_size = '12pt'
    p_means.yaxis.axis_label = 'Velocity (microns/sec)'
    p_means.xaxis.axis_label = 'Time (hr)'

    for p in [p0, p1, p2, p4, p8]:
        p.add_tools(hover)
        p.yaxis.major_label_text_font_size = "12pt"
        p.xaxis.major_label_text_font_size = "12pt"
        p.legend.location = "top_right"
        p.legend.click_policy = "hide"
        p.legend.label_text_font_size = '8pt'
        p.title.text_font_size = '12pt'

    for p in [p0, p4]:
        p.yaxis.axis_label = 'Frequency'
        p.yaxis.axis_label_text_font_size = "12pt"
        p.yaxis.axis_label_text_font = "times"
        p.yaxis.axis_label_text_font_style = 'normal'

    for p in [p4, p8]:
        p.xaxis.axis_label = 'Velocity (microns/sec)'
        p.xaxis.axis_label_text_font_size = "12pt"
        p.xaxis.axis_label_text_font = "times"
        p.xaxis.axis_label_text_font_style = 'normal'

    for p in [p1, p2, p8]:
        p.yaxis.major_label_text_font_size = '0pt'

    for p in [p0, p1, p2]:
        p.xaxis.major_label_text_font_size = '0pt'
   

    grid = gridplot([
        [p0, p1, p2],
        [p4, p8, p_means]
    ])

    return grid
