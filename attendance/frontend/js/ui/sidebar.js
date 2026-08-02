import {state} from "../state.js";

export function renderSidebar(onSelect)
{

    const list = document.getElementById("imageList");

    list.innerHTML = "";

    state.images.forEach((image,index)=>{

        const li = document.createElement("li");

        li.className = "image-item";

        if(index===state.currentIndex)
            li.classList.add("selected");

        li.innerHTML = `
            <div>${image.filename}</div>
            <small>${image.status}</small>
        `;

        li.onclick=()=>onSelect(index);

        list.appendChild(li);

    });

}
