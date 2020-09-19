var script = document.createElement('script');
script.type = 'text/javascript';
script.src = "https://cdn.ckeditor.com/4.14.1/standard-all/ckeditor.js";
document.head.appendChild(script);

script.onload = function() {
    CKEDITOR.replace('id_description', {
        width: '100%',
        height: 300
    });
    config.extraPlugins = 'autogrow';
    config.autoGrow_minHeight = 200;
    config.autoGrow_maxHeight = 600;
    config.autoGrow_bottomSpace = 50;
};