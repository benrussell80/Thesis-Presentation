from flask import Blueprint, render_template
from glob import glob
import os
import json
from bokeh.embed import json_item
from .plot_generators import od_plot_generator, velocity_hists_generator


slides = Blueprint('slides', __name__)

slide_mapper = [
    'title.html',
    'antibiotic_resistance_crisis_1.html',
    'antibiotic_resistance_crisis_2.html',
    'antibiotic_resistance_crisis_3.html',
    'silver_as_an_antimicrobial.html',
    'pathogenic_e_coli.html',
    'e_coli_banner.html',
    'e_coli_as_a_model_organism_1.html',
    'e_coli_as_a_model_organism_2.html',
    'goal.html',
    'experimental_design_overview.html',
    'findings.html',
    'findings1.html',
    'swimming_assay_results.html',
    'swimming_assay_methods_1.html',
    'swimming_assay_methods_2.html',
    'swimming_assay_methods_3.html',
    'swimming_assay_od_600.html',
    'swimming_assay_data_processing_1.html',
    'swimming_assay_data_processing_2.html',
    'swimming_assay_data_processing_3.html',
    'swimming_assay_data_processing_4.html',
    'swimming_assay_data_processing_5.html',
    'swimming_assay_data_processing_6.html',
    'swimming_assay_selected_track_results_1.html',
    'swimming_assay_selected_track_results_2.html',
    'swimming_assay_selected_track_velocities.html',
    'findings1.html',
    'findings2.html',
    'swimming_assay_car_explanation.html',
    'swimming_assay_selected_track_car.html',
    'swimming_assay_msd_vs_tau_1.html',
    'swimming_assay_msd_vs_tau_2.html',
    'swimming_assay_conclusions.html',
    'findings3.html',
    'tethering_assay_results.html',
    'tethering_assay_imaging_protocol.html',
    'tethering_assay_data_processing.html',
    'tethering_assay_rolling_mean_of_omega_vs_time.html',
    'tethering_assay_histograms_of_omega.html',
    'tethering_assay_question.html',
    'the_hidden_markov_model_1.html',
    'the_hidden_markov_model_2.html',
    'tethering_assay_gaussian_hmm.html',
    'tethering_assay_predict_run_tumble_states_with_hmm.html',
    'tethering_assay_changes_to_hmm_parameters.html',
    'tethering_assay_conclusions.html',
    'summary_of_findings.html',
    'future_research.html',
    'acknowledgments.html',
    'citations.html'
]

@slides.route('/')
def index():
    return render_template('index.html')

@slides.route('/slide/<int:number>')
def slide_number(number):
    number = max(number, 0)
    return render_template(slide_mapper[number], slide_number=number, number_of_slides=len(slide_mapper))

@slides.route('/od-plot')
def od_plot():
    p = od_plot_generator()
    return json.dumps(json_item(p))

@slides.route('/velocity-plot')
def velocity_plot():
    p = velocity_hists_generator()
    return json.dumps(json_item(p))