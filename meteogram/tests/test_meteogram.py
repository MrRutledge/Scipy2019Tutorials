"""Test use of the meteogram module."""

from meteogram import meteogram
import datetime
import numpy as np
from numpy.testing import assert_almost_equal, assert_array_almost_equal
from unittest.mock import patch
import pytest
from pathlib import  Path 

@pytest.fixture
def laod_example_asos():
    """
    Fixture to load example data 
    """

    example_data_path = Path(__file__).resolve().parent /'..'/'staticdata'
    data_path = example_data_path / 'AMW_example_data.csv'

    return meteogram.download_asos_data(data_path)

#
# Example starter test
#
def test_degF_to_degC_at_freezing():
    """
    Test if celsius conversion is correct at freezing.
    """
    # Setup
    freezing_degF = 32.0
    freezing_degC = 0.0

    # Exercise
    result = meteogram.degF_to_degC(freezing_degF)

    # Verify
    assert result == freezing_degC

    # Cleanup - none necessary

#
# Instructor led introductory examples
#

def test_title_case():
    # setup
    in_string = 'this is a test string'
    desired  = 'This Is A Test String'

    #excercise
    actual = in_string.title()

    #Verify
    assert actual == desired 
#
# Instructor led examples of numerical comparison
#

#
# Exercise 1
#
def test_build_asos_request_url_single_digit_datetimes():
    """
    Test building URL with single digit month and day.
    """
    # Setup 
    start = datetime.datetime(2018, 1,5,1)
    end = datetime.datetime(2018,1,9,1)
    station = 'FSD'

    #Exercise
    result_url = meteogram.build_asos_request_url(station, start, end)

    #verify
    truth_url = 'https://mesonet.agron.iastate.edu/request/asos/1min_dl.php?station%5B%5D=FSD&tz=UTC&year1=2018&month1=01&day1=05&hour1=01&minute1=00&year2=2018&month2=01&day2=09&hour2=01&minute2=00&vars%5B%5D=tmpf&vars%5B%5D=dwpf&vars%5B%5D=sknt&vars%5B%5D=drct&sample=1min&what=view&delim=comma&gis=yes'
    assert result_url == truth_url

    # cleanup = none 


def test_build_asos_request_url_double_digit_datetimes():
    """
    Test building URL with double digit month and day.
    """
     # Setup 
    start = datetime.datetime(2018, 10,11,11)
    end = datetime.datetime(2018,10,16,11)
    station = 'FSD'

    #Exercise
    result_url = meteogram.build_asos_request_url(station, start, end)

    #verify
    truth_url = 'https://mesonet.agron.iastate.edu/request/asos/1min_dl.php?station%5B%5D=FSD&tz=UTC&year1=2018&month1=10&day1=11&hour1=11&minute1=00&year2=2018&month2=10&day2=16&hour2=11&minute2=00&vars%5B%5D=tmpf&vars%5B%5D=dwpf&vars%5B%5D=sknt&vars%5B%5D=drct&sample=1min&what=view&delim=comma&gis=yes'
    assert result_url == truth_url

    # cleanup = none 

#
# Exercise 1 - Stop Here
#
def test_does_three_equal_three():
    assert 33 == 33

def test_flaoting_subtraction():
    # Setup
    desired  = 0.293
    #Exercise
    actual = 1-0.707
    #Verify

    #assert (abs(actual == desired)< 0.00001)
    assert_almost_equal(actual, desired)#optianal arg
    #Cleanup = none

#
# Exercise 2 - Add calculation tests here
#
def test_wind_components_north():
    #setup
    speed = 10
    direction = 0

    #Exercise
    u,v = meteogram.wind_components(speed, direction)

    #Verify
    true_u = 0
    true_v = -10
    assert_almost_equal(u, true_u)
    assert_almost_equal(v, true_v)

def test_wind_components_northwest():
    #setup
    speed = 10
    direction = 45

    #Exercise
    u,v = meteogram.wind_components(speed, direction)

    #Verify
    true_u = -7.0710
    true_v = -7.0710
    assert_almost_equal(u, true_u,4)
    assert_almost_equal(v, true_v,4)

#
# Exercise 2 - Stop Here
#
def test_wind_components():
    #Setup
    speed = np.array([10,10,10,0])
    direction = np.array([0,45,360,45])

    #Excersise 
    u,v = meteogram.wind_components(speed, direction)

    #Verify
    true_u = np.array([0, -7.0710, 0 ,0])
    true_v = np.array([-10,-7.0710,-10,0])
    assert_array_almost_equal(u, true_u, 3)
    assert_array_almost_equal(v,true_v, 3)

    #Cleanup = None

#
# Instructor led mock example
#
def mocked_current_utc_time():
    """
    Mock our utc time function for testing with defaults.
    """
    # Setup
    return datetime.datetime(2018,3,26,12)

@patch('meteogram.meteogram.current_utc_time', new = mocked_current_utc_time)
def test_that_mock_works():
    """
    Test if we really know how to use a mock
    """

    # Setup - None
    # Excercise 
    result = meteogram.current_utc_time()
    # Verify
    truth = datetime.datetime(2018,3,26,12)
    assert  result == truth

#
# Exercise 3
#
@patch('meteogram.meteogram.current_utc_time',new=mocked_current_utc_time)
def test_build_asos_request_url_default():
    #Setup  - none

    #exercise
    url = meteogram.build_asos_request_url('MLI')

    # Verify
    truth  = 'https://mesonet.agron.iastate.edu/request/asos/1min_dl.php?station%5B%5D=MLI&tz=UTC&year1=2018&month1=03&day1=25&hour1=12&minute1=00&year2=2018&month2=03&day2=26&hour2=12&minute2=00&vars%5B%5D=tmpf&vars%5B%5D=dwpf&vars%5B%5D=sknt&vars%5B%5D=drct&sample=1min&what=view&delim=comma&gis=yes'
    assert url == truth

#
# Exercise 3 - Stop Here
#


#
# Exercise 4 - Add any tests that you can to increase the library coverage.
# think of cases that may not change coverage, but should be tested
# for as well.
#
def test_current_utc_time():
    #setup
    #Excercise
    result = meteogram.current_utc_time()

    # verify
    truth = datetime.datetime.utcnow()
    assert result.replace(microsecond=0)==truth.replace(microsecond=0)
#
# Exercise 4 - Stop Here
#

#
# Instructor led example of image testing
#
@pytest.mark.mpl_image_compare(remove_text=True, tolerance=0)
def test_plotting_meteogram_defaults(laod_example_asos):
    # Setup

    #url= meteogram.build_asos_request_url('AMW',
     #   start_date= datetime.datetime(2018,3,26),
      #  end_date=datetime.datetime(2018,3,27))

    #df = meteogram.download_asos_data(url)
    # Excercise

    fig,_, _,_ = meteogram.plot_meteogram(laod_example_asos)

    # Verify - Done elsewhere

    # Cleanup

    return fig


#
# Exercise 5
#

#
# Exercise 5 - Stop Here
#

#
# Exercise 6
#

#
# Exercise 6 - Stop Here
#

#
# Exercise 7
#

#
# Exercise 7 - Stop Here
#

# Demonstration of TDD here (time permitting)
