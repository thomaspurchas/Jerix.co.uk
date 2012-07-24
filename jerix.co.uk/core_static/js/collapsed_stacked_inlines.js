/* collapsed_stacked_inlines.js */
/* Created in May 2009 by Hannes Rydén */
/* Use, distribute and modify freely */

django.jQuery(document).ready(function() {
	$ = django.jQuery;
    // Only for stacked inlines
	console.log('Hey there');
	console.log($('div.inline-group'))
    $('div.inline-group, div.inline-related:not(.tabular)').each(function() {
        fs = $(this).find('fieldset');
        h3 = $(this).find('h2:first');

        // Don't collapse if fieldset contains errors
        if (fs.find('div').hasClass('errors'))
            fs.addClass('stacked_collapse');
        else
            fs.addClass('stacked_collapse collapsed');

        // Add toggle link
        h3.append(' (<a class="collapse-toggle" href="#">' + gettext('Show') + '</a>)');
        h3.find('a.collapse-toggle').bind("click", function(){
            fs = $(this).parent('h2').parent('fieldset');
            if (!fs.hasClass('collapsed'))
            {
                fs.addClass('collapsed');
                $(this).html('' + gettext('Show') + '');
            }
            else
            {
                fs.removeClass('collapsed');
                $(this).html('' + gettext('Hide') + '');
            }
        }).removeAttr('href').css('cursor', 'pointer').css('color', '#5B80B2');
    });
});