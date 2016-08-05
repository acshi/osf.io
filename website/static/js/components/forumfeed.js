/**
* Mithril component to show latest topic excerpts from the forum.
*/
'use strict';
var $ = require('jquery');
var m = require('mithril');
var Raven = require('raven-js');
var utils = require('js/components/utils');
var required = utils.required;

require('css/forum-feed.css');

var ForumFeed = {
    controller: function(options) {
        var self = this;
        self.loading = true;
        self.failed = false;
        self.node = required(options, 'node');
        self.user = required(options, 'user');
        self.discourse_url = required(options, 'discourse_url');
        self.user_apikey = required(options, 'discourse_user_apikey');
        var requestUrl = self.discourse_url + '/forum/' + self.node.id + '/latest.json';
        var data = { api_key: self.user_apikey, api_username: self.user.id };
        m.request({method : 'GET', url : requestUrl, data: data}).then(function(results) {
            self.topics = results.topic_list.topics;
            self.usernamesToNames = {};
            results.users.forEach(user => {
                self.usernamesToNames[user.username] = user.name;
            });
            self.topics.forEach(topic => {
                if (topic.excerpt_mentioned_users) {
                    topic.excerpt_mentioned_users.forEach(user => {
                        self.usernamesToNames[user.username] = user.name;
                    });
                }
            });
            results.topic_list.contributors.forEach(contributor => {
                self.usernamesToNames[contributor.username] = contributor.name;
            });
            self.topics.forEach(topic => {
                if (!topic.excerpt) {
                    topic.excerpt = '';
                    return;
                }
                var excerpt = topic.excerpt;
                var mentions = topic.excerpt.match(/@[a-z0-9]+/g);
                if (mentions) {
                    mentions.forEach(mention => {
                        var username = mention.substr(1);
                        if (self.usernamesToNames[username]) {
                            excerpt = excerpt.replace(mention, '@' + self.usernamesToNames[username]);
                            excerpt = excerpt.replace('href="/users', 'href="' + self.discourse_url + '/users');
                        }
                    });
                    topic.excerpt = excerpt;
                }
            });
            self.loading = false;
        }, function(xhr, textStatus, error) {
            self.failed = true;
            self.loading = false;
            var message = 'Error retrieving latest forum topics for ' + self.node.id;
            Raven.captureMessage(message, {extra: {url: requestUrl, textStatus: textStatus, error: error}});
        });
    },
    view: function(ctrl, options) {
        var self = this;
        return m('div.forum-feed ', [
            ctrl.failed ? m('p', [
                'Unable to retrieve forum topics at this time. Please refresh the page or contact ',
                m('a', {'href': 'mailto:support@osf.io'}, 'support@osf.io'),
                ' if the problem persists.'
            ]) :
            // Show OSF spinner while there is a pending log request
            ctrl.loading ? m('.spinner-loading-wrapper', [
                m('.logo-spin.logo-lg'),
                m('p.m-t-sm.fg-load-message', 'Loading forum topics...')
            ]) :
            m('table', m('tbody', ctrl.topics.slice(0, 5).map(topic => {
                var postNumber = topic.highest_post_number;
                if (topic.last_read_post_number) {
                    postNumber = Math.min(topic.last_read_post_number + 1, topic.highest_post_number);
                }
                var postUrl = ctrl.discourse_url + '/t/' + topic.slug + '/' + topic.id + '/' + postNumber;
                var projectUrl = ctrl.discourse_url + '/forum/' + topic.project_guid;
                return m('tr',
                    m('td', [
                        m('a.title', {href: postUrl}, topic.fancy_title),
                        m('div.osf-parent-project',
                            m('a', {href: projectUrl}, topic.project_name)
                        ),
                        m('div.topic-excerpt', m.trust(topic.excerpt))
                    ])
                );
            })))
        ]);
    }
};

module.exports = {
    ForumFeed: ForumFeed,
};
