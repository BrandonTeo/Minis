// Assign eventListener to our form
document.getElementById('input-form').addEventListener('submit', geocode);

function geocode(e) {
    // Intercept the form submission
    e.preventDefault();

    // Obtain the input from form
    var input = document.getElementById('input-address').value;

    // Call to api
    axios.get('https://maps.googleapis.com/maps/api/geocode/json', {
        params: {
            address: input,
            key: '<API-KEY-HERE>'
        }

    }).then(function(res) {
        // Output formatted address
        var f_add = res.data.results[0].formatted_address;
        var f_add_output = `
            <div class="titles">Formatted Address: </div>
            <p>${f_add}</p>
        `;
        document.getElementById('formatted').innerHTML = f_add_output;

        // Output address components
        var add_comps = res.data.results[0].address_components // List
        var add_comps_output = `
            <div class="titles">Address Components: </div>
            <ul>
        `;
        for(var i = 0; i < add_comps.length; i++) {
            add_comps_output += `
                <li><strong>${add_comps[i].types[0]}:</strong> ${add_comps[i].long_name}</li>
            `;
        }
        add_comps_output += `</ul>`;
        document.getElementById('components').innerHTML = add_comps_output;

    }).catch(function(err) {
        console.log(err);
        
    });
}
