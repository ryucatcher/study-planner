
function makeRequest(csrf){
    axios.post('/api/updatedeadlinename', {
        userid: 1234,
        test: 'test'
    }, {
        headers:{
            'X-CSRFToken': csrf
        },
        data:{
            test2: 'test'
        }
    }).then(function (response){
        console.log(response);
    });
}