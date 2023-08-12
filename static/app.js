function get_cupcake_html(cupcake){
    return `
        <div data-cupcake_id="${cupcake.id}">
            <li>${cupcake.flavor} // ${cupcake.size} // ${cupcake.rating} // <button class="delete">X</button></li>
            <img src="${cupcake.image}" alt="${cupcake.flavor} cupcake">
        </div>
    `;
}

function get_cupcake_form_data(){
    let data;
    if ($('#image').val() == ""){
        data = {
            "flavor": $('#flavor').val(),
            "size": $("input[name='size']:checked").val(),
            "rating": $('#rating').val(),
        }
    } else {
        data = {
        "flavor": $('#flavor').val(),
        "size": $("input[name='size']:checked").val(),
        "rating": $('#rating').val(),
        "image": $('#image').val()
        }
    }
    return data;
}

function apply_delete_func(){
    $('.delete').on('click', function(e){
        id = $(this).parent().parent()[0].dataset.cupcake_id;
        delete_cupcake(id);
    })
}

async function show_cupcakes(){
    const res = await axios.get("/api/cupcakes");
    const cc = res.data.cupcakes;
    for(let c of cc){
        let new_cc = get_cupcake_html(c);
        $("#cc_list").append(new_cc);
    }
    apply_delete_func();
}

async function add_cupcake(){
    data = get_cupcake_form_data()
    const res = await axios.post("/api/cupcakes", data);
    const cupcake_obj = res.data.cupcake[0];

    new_cc = get_cupcake_html(cupcake_obj);
    $("#cc_list").append(new_cc);
    apply_delete_func();
}

async function delete_cupcake(id){
    const res = await axios.delete(`/api/cupcakes/${id}`);
    $(`div[data-cupcake_id=${id}]`).remove();
}

$(show_cupcakes);

$('form').on('submit', function(e){
    e.preventDefault();
    add_cupcake();
    $(this).trigger('reset');
})


