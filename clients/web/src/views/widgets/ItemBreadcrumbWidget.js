var $      = require('jquery');
var girder = require('girder/init');
var View   = require('girder/view');

require('bootstrap/js/tooltip');

var IteamBreadcrumbTemplate = require('girder/templates/widgets/itemBreadcrumb.jade');

/**
 * Renders the a breadcrumb for the item page
 */
var ItemBreadcrumbWidget = View.extend({
    events: {
        'click a.g-item-breadcrumb-link': function (event) {
            var link = $(event.currentTarget);
            girder.router.navigate(link.data('type') + '/' + link.data('id'),
                                   {trigger: true});
        },
        'click a.g-hierarchy-level-up': function () {
            var folder = this.parentChain.pop().object;
            girder.router.navigate('folder/' + folder._id, {trigger: true});
        }
    },

    initialize: function (settings) {
        this.parentChain = settings.parentChain;
        this.render();
    },

    render: function () {
        this.$el.html(IteamBreadcrumbTemplate({
            parentChain: this.parentChain
        }));

        this.$('.g-hierarchy-level-up').tooltip({
            container: this.$el,
            placement: 'left',
            animation: false,
            delay: {show: 100}
        });
    }
});

module.exports = ItemBreadcrumbWidget;
