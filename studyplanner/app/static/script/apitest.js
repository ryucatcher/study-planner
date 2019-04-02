
function getUserProfile(csrf){
    console.log(Cookies.get('userid'));
    axios.post('/api/getstudyprofile', {
        userid: Cookies.get('userid'),
        year: 2
    }, {
        headers:{
            'X-CSRFToken': csrf
        }
    }).then(function (response){
        data = response.data
        resultContainer = $('#user-profile-content');
        if(data.error && data.error.length > 0){
            data.error.forEach(error => {
                resultContainer.append(`<p class="text-danger">${error}</p>`)
            });
        }
        console.log(data)
    });
}