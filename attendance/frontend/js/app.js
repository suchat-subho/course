import * as API from "./api.js";

import {state} from "./state.js";

import {renderSidebar} from "./ui/sidebar.js";

window.addEventListener("DOMContentLoaded",async()=>{

    await API.initialize();

    renderSidebar(selectImage);

});

function selectImage(index)
{

    state.currentIndex=index;

    console.log(state.images[index]);

    renderSidebar(selectImage);

}
