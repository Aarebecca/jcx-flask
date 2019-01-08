function getQueryletiable(param) {// 查询url参数
       let query = window.location.search.substring(1);
       let vars = query.split("&");
       for (let i = 0;i < vars.length;i++) {
               let pair = vars[i].split("=");
               if(pair[0] == param){
                   return pair[1];
                }
       }
       return(false);
}