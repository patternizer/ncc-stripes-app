![image](https://github.com/patternizer/ncc-stripes-app/blob/main/PLOTS/mural-app-climate-analogues.png)

# ncc-stripes-app

Python code to merge geological, instrumental and climate model global land surface air temperature anomalies and visualise them with an interactive interface. See the website of [Climate Mural for our Times](https://crudata.uea.ac.uk/cru/climate-mural/index.html) for more information about the mural installed in the debating chamber of Norwich City Council.
  
## Contents

* `app.py` - Plotly python Dash app that runs off Flask.

The first step is to clone the latest ncc-stripes-app code and step into the check out directory: 

    $ git clone https://github.com/patternizer/ncc-stripes-app.git
    $ cd ncc-stripes-app
    
### Using Standard Python 

The code should run with the [standard CPython](https://www.python.org/downloads/) installation and was tested in a conda virtual environment running a 64-bit version of Python 3.8.11+.

ncc-stripes-app can be run from sources directly. The data in /OUT is generated independently in the repo: ncc-stripes. 

Run an instance of the app in your localhost with:

    $ python app.py
            
## License

The code is distributed under terms and conditions of the Attribution 4.0 International (CC BY 4.0) license: https://creativecommons.org/licenses/by/4.0/.

## Contact information

* [Michael Taylor](https://patternizer.github.io)


