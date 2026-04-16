from flask import Flask, render_template, request

app = Flask(__name__)

# This dictionary helps the HTML know which units to show in the dropdowns
UNITS_CONFIG = {
    'length': ['meters', 'feet', 'millimeter', 'centimeter', 'kilometer', 'inch', 'yard', 'mile'],
    'weight': ['kilograms', 'pounds', 'milligram', 'gram', 'ounce'],
    'temperature': ['celsius', 'fahrenheit', 'kelvin']
}

@app.route('/')
@app.route('/<category>', methods=['GET', 'POST'])
def index(category='length'):
    # Default to 'length' if the user visits a category not in our list
    if category not in UNITS_CONFIG:
        category = 'length'
    
    # Get the units for the current selected category
    units = UNITS_CONFIG[category]
    
    result = None
    val = None
    from_u = None
    to_u = None

    if request.method == 'POST':
        # Grab data from the HTML form
        try:
            val = float(request.form.get('value', 0))
            from_u = request.form.get('from_unit')
            to_u = request.form.get('to_unit')

            # --- YOUR LOGIC START ---
            if from_u == "meters" and to_u == "feet":
                res_val = val * 3.28084
            elif from_u == "feet" and to_u == "meters":
                res_val = val / 3.28084
            elif from_u == "kilograms" and to_u == "pounds":
                res_val = val * 2.20462
            elif from_u == "pounds" and to_u == "kilograms":
                res_val = val / 2.20462
            elif from_u == "celsius" and to_u == "fahrenheit":
                res_val = (val * 9/5) + 32
            elif from_u == "fahrenheit" and to_u == "celsius":
                res_val = (val - 32) * 5/9
            # Adding Kelvin for the roadmap requirements
            elif from_u == "celsius" and to_u == "kelvin":
                res_val = val + 273.15
            elif from_u == "kelvin" and to_u == "celsius":
                res_val = val - 273.15
            else:
                res_val = "Conversion logic not yet implemented for these specific units."
            # --- YOUR LOGIC END ---

            if isinstance(res_val, (int, float)):
                result = f"{val} {from_u} is equal to {round(res_val, 4)} {to_u}."
            else:
                result = res_val

        except ValueError:
            result = "Please enter a valid number."

    return render_template('index.html', 
                           category=category, 
                           units=units, 
                           result=result)

if __name__ == '__main__':
    app.run(debug=True)