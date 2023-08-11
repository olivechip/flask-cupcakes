function get_cupcake_html(cupcake){
    return `
        <div data-cupcake_id="${cupcake.id}">
            <li>${cupcake.flavor} // ${cupcake.size} // ${cupcake.rating}</li>
            <img src="${cupcake.image}">
        </div>
    `;
}

async function show_cupcakes(){
    const res = await axios.get("/api/cupcakes");
    const cc = res.data.cupcakes;
    for(let c of cc){
        let new_cc = get_cupcake_html(c);
        $("#cc_list").append(new_cc);
    } 
}

async function add_cupcake(){
    data = {
        "flavor": $('#flavor').val(),
        "size": $("input[name*='size'").val(),
        "rating": $('#rating').val(),
        "image": $('#image').val()
    }
    console.log(data)
    const res = await axios.post("/api/cupcakes", data);
    const cc = res.data.cupcakes;
    // console.log(cc);
    // alert('created');
}

$(show_cupcakes);

$('form').on('submit', function(e){
    e.preventDefault();
    add_cupcake();
})

