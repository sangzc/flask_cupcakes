BASE_URL = 'http://localhost:5000'

$(function(){

    $flavor = $('#cupcakeFlavor')
    $size = $('#cupcakeSize')
    $rating = $('#cupcakeRating')
    $imageUrl = $('#cupcakeImageURL')
    $form = $('#cupcakeForm')
    $cupcakeList = $('#listOfCupcakes')


    createCupcakeList();

    async function createCupcakeList(){

        let response = await $.get('/cupcakes')
        let cupcakeList = response.response

        for (let cupcake of cupcakeList){
            appendCupcake(cupcake)
        }

    }

    function appendCupcake(cupcake){
        let single_cupcake = $('<li>').text(`${cupcake.flavor} cupcake is ${cupcake.size} and is rated ${cupcake.rating} stars.`)
            $cupcakeList.append(single_cupcake)
    }
    


    $form.on('submit', async function submitNewCupcake(evt){

        evt.preventDefault();

        let flavor = $flavor.val();
        let size = $size.val();
        let rating = $rating.val();
        let image = ($imageUrl.val().length > 0) ? $imageUrl.val() : null
        
        let response_data = await $.ajax({method: "POST",
                                     url: `${BASE_URL}/cupcakes`,
                                     contentType: "application/json",
                                     data: JSON.stringify({
                                         "flavor":flavor,
                                         "size":size,
                                         "rating":rating,
                                         "image":image
                                        }),
                                    });
        
        appendCupcake(response_data.response)

    })

    






})