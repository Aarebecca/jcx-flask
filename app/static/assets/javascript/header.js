let str1 = " ",
    str2 = " ",
    str3 = " ",
    html = " ";
for(let i = 0; i < head_menue.length - 1; i++) { // head_menue.length - 1 校企合作不是头部导航
    let sub_menue = head_menue[i].sub_menue;
    if(sub_menue.length === 0) {
        str1 = `<li class="left">
        <a href=${head_menue[i].link}?id=${head_menue[i].id}>${head_menue[i].name}</a>
        <div class="sub_menue absolute">`;
        str2 = " "
    } else {
        str1 = `<li class="left relative">
        <a href="javascript:;">${head_menue[i].name}</a>
        <div class="sub_menue absolute">`;
        str2 = " ";
        for(let j = 0; j < sub_menue.length; j++) {
            str2 += `<div class="item_tr">
                    <a href="jzclgcx.html?id=${head_menue[i].id}&kw=${head_menue[i].kw[j]}">${sub_menue[j]}</a>
                    </div>`
        }
    }
    str3 = `</div></li>`;
    html += str1 + str2 + str3;
}


