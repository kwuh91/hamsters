"use strict";

(function () {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
            }

            form.classList.add('was-validated')
        }, false)
        })
})()

/////////////////////////

document.getElementById('show_period').addEventListener('change', function () {
    var periodFields = document.getElementById('period_fields');
    periodFields.style.display = this.checked ? 'block' : 'none';
    document.getElementById('start_date').disabled = !this.checked;
    document.getElementById('end_date').disabled = !this.checked;
});

document.getElementById('resetButton').addEventListener('click', function() {
       document.forms[1].reset(); 
       document.forms[1].submit();
});

/////////////////////////////

    // Initialize Select2 on your dropdown
    $(document).ready(function() {
        $('#client').select2({
            theme: 'bootstrap-5',
            containerCssClass: 'form-select custom-font' // Manually add form-select and custom-font classes
        });
        $('#salon').select2({
            theme: 'bootstrap-5',
            containerCssClass: 'form-select custom-font' // Manually add form-select and custom-font classes
        });
    });

    "use strict";

    (function () {
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.querySelectorAll('.needs-validation')

        // Loop over them and prevent submission
        Array.prototype.slice.call(forms)
            .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
                }

                form.classList.add('was-validated')
            }, false)
            })
    })()

    "use strict";

    Array.from(document.getElementsByClassName('showmodal')).forEach((e) => {
        e.addEventListener('click', function (element) {
            element.preventDefault();
            if (e.hasAttribute('data-show-modal')) {
                const animalType = e.getAttribute('data-animal-type');
                showModal(e.getAttribute('data-show-modal'), animalType);
            }
        });
    });

    // Show modal dialog
    function showModal(modal, animalType) {
        const mid = document.getElementById(modal);
        let myModal = new bootstrap.Modal(mid);

        // Fetch services for the clicked image using AJAX
        fetch(`/get_services/${animalType}/`)
            .then(response => response.json())
            .then(data => {
                // Update modal content with services
                const modalBody = document.getElementById('servicesModalBody');
                modalBody.innerHTML = '';  // Clear existing content

                // Create a FormData object to collect form data
                var formData = new FormData();

                // Append the CSRF token to the FormData
                const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
                formData.append('csrfmiddlewaretoken', csrfToken);

                // Append the animal_type to the FormData
                formData.append('animal_type', animalType);
                
                let service_count_map = {};
                data.services.forEach(service => {
                    const serviceItem = document.createElement('div');
                    serviceItem.classList.add("row", "mb-3", "service-item");
                    serviceItem.innerHTML = 
                    `
                    <div class="col-md-6">
                        <strong>${service.name}</strong>: ${service.price}$
                    </div>
                    <div class="col-md-6 text-end">
                        <button type="button" class="btn btn-danger" id="minus-btn${service.id}">-</button>
                        <span class="mx-2" id="modal-number${service.id}">0</span>
                        <button type="button" class="btn btn-success" id="plus-btn${service.id}">+</button>
                    </div>
                    `;

                    modalBody.appendChild(serviceItem);

                    // Add event listeners for plus and minus buttons
                    const minusBtn = document.getElementById(`minus-btn${service.id}`);
                    const plusBtn = document.getElementById(`plus-btn${service.id}`);
                    const modalNumberSpan = document.getElementById(`modal-number${service.id}`);

                    let count = 0;
                    service_count_map[`service_count${service.id}`] = 0;

                    minusBtn.addEventListener('click', () => {
                        if (count > 0) {
                            count--;
                            modalNumberSpan.innerText = count;
                            service_count_map[`service_count${service.id}`] = count;  // Update hidden input value
                            // console.log(count,`minus-btn-count for ${service.name}`);
                        }
                    });

                    plusBtn.addEventListener('click', () => {
                        count++;
                        modalNumberSpan.innerText = count;
                        service_count_map[`service_count${service.id}`] = count;  // Update hidden input value
                        // console.log(count,`plus-btn-count for ${service.name}`);
                    });

                    // const quantity = count || 0;

                    // Append the service_count input to FormData
                    // console.log(count,`pre-append-count for ${service.name}`);
                    // formData.append(`service_count${service.id}`, count);
                    // console.log(count,`post-append-count for ${service.name}`);
                });

                // Display the modal
                myModal.show();

                // Add event listener to the form submission inside the modal
                document.getElementById('update_cart').addEventListener('submit', function (event) {
                    // Log the object to see its contents
                    console.log("Object after adding data:", service_count_map);
                    let send_request = false;
                    // Append the service_count inputs to FormData
                    for (let key in service_count_map) {
                        console.log(`Value at key ${key}:`, service_count_map[key]);
                            // Check if service_count_map[key] is not equal to 0
                            if (service_count_map[key] !== 0) {
                                formData.append(key, service_count_map[key]);
                                send_request = true;
                            }
                    }
                    service_count_map = {};

                    // Prevent the default form submission
                    event.preventDefault();

                    // Check if formData is not empty
                    if (formData && formData.entries().next().done === false && send_request) {
                        // Make an AJAX request to submit the form data
                        fetch('/update_cart/', {
                            method: 'POST',
                            body: formData
                        })
                        .then(response => response.json())
                        .then(data => {
                            // Handle the response if needed
                            console.log(data);

                            // for (var item of formData.keys()) {
                            //     formData.delete(item)
                            // };

                            // clear the form data
                            formData = new FormData();
                            myModal.hide();
                        })
                        .catch(error => console.error('Error updating cart:', error));
                    } else {
                        // Handle the case where formData is empty, if needed
                        console.log('Form data is empty. No request sent.');
                    }
                });
            })
            .catch(error => console.error('Error fetching services:', error));
    }

    document.addEventListener('DOMContentLoaded', function () {
        // Add event listener to the client dropdown
        document.getElementById('client').addEventListener('change', function () {
            // Check if the selected option is 'Add New'
            if (this.value === 'add_new') {
                // Show the modal
                var addNewClientModal = new bootstrap.Modal(document.getElementById('addNewClientModal'));
                addNewClientModal.show();
            }
        });

        // Add event listener to the form submission
        document.getElementById('clientForm').addEventListener('submit', function (event) {
            // Prevent the default form submission
            event.preventDefault();

            // You can add your logic to handle the form submission (e.g., AJAX request to save the new client)
            
            // Collect form data
            var formData = {
                'name': $('#newClientName').val(),
                'phone': $('#newClientPhone').val(),
                'email': $('#newClientEmail').val()
            };
            
            // Get the CSRF token from the page's cookies
            var csrftoken = Cookies.get('csrftoken'); 

            // Send AJAX request
            $.ajax({
                type: 'POST',
                url: '/save-client/',  // Replace with your actual URL
                data: formData,
                beforeSend: function (xhr) {
                    // Include the CSRF token in the request headers
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                },
                success: function (data) {
                    // Handle success, if needed
                    console.log('Client saved successfully');
                    
                    // Clear form fields
                    $('#newClientName').val('');
                    $('#newClientPhone').val('');
                    $('#newClientEmail').val('');

                    // Close the modal
                    var addNewClientModal = new bootstrap.Modal(document.getElementById('addNewClientModal'));
                    addNewClientModal.hide();
                },
                error: function (data) {
                    // Handle errors, if needed
                    console.error('Error saving client');
                }
            });

        });
    });

    // Add event listener to the form submission
    document.getElementById('show_final_price').addEventListener('submit', function (event) {
            // Prevent the default form submission
            event.preventDefault();

            // You can add your logic to handle the form submission (e.g., AJAX request to save the new client)
            
            // Collect form data
            var formData = {
                'salon': document.getElementById('salon').value,
                'client': document.getElementById('client').value
            };
            
            // Get the CSRF token from the page's cookies
            var csrftoken = Cookies.get('csrftoken'); 

            // Send AJAX request
            $.ajax({
                type: 'POST',
                url: '/show_final_price/',  // Replace with your actual URL
                data: formData,
                beforeSend: function (xhr) {
                    // Include the CSRF token in the request headers
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                },
                success: function (data) {
                    console.log("Success showing final price");
                    console.log(data);
                    // Update modal content with services
                    const modalBody = document.getElementById('FinalPriceBody');
                    modalBody.innerHTML = '';  // Clear existing content
                    const priceItem = document.createElement('div');
                    // priceItem.classList.add("row", "mb-3");
                    priceItem.innerHTML = 
                    `
                    <strong>price</strong>: ${data.final_price}$
                    `;
                    modalBody.appendChild(priceItem);
                    // Close the modal
                    // var addNewClientModal = new bootstrap.Modal(document.getElementById('addNewClientModal'));
                    // addNewClientModal.hide();
                },
                error: function (data) {
                    // Handle errors, if needed
                    console.log(data);
                    console.error('Error showing final price');
                }
            });

        });
