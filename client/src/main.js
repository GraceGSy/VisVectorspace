import App from './App.svelte';

var DEBUG = false;
if(!DEBUG){
    if(!window.console) window.console = {};
    var methods = ["debug", "warn", "info"];
    for(var i=0;i<methods.length;i++){
        console[methods[i]] = function(){};
    }
}

var app = new App({
	target: document.body
});

export default app;