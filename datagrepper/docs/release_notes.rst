=============
Release Notes
=============

.. towncrier release notes start

v1.0.1
======

Released on 2023-09-22.
This is a feature & bugfix release.

Features
^^^^^^^^

* Add a link to the list of available topics (:issue:`291`).

Bug Fixes
^^^^^^^^^

* Fix the documentation generation on the front page (:issue:`537`).


v1.0.0
======

Released on 2022-01-17.
This is a major release that rebases on datanommer's port to TimescaleDB.

Backwards Incompatible Changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Drop the ``grouped`` argument feature, as fedora-messaging does not support
  it (:issue:`264`).

Development Improvements
^^^^^^^^^^^^^^^^^^^^^^^^

* Drop the dependency on fedmsg (:issue:`264`).


Thanks to all contributors who made this release possible!


0.9.7
=====

Pull Requests

- Fix bug introduced with the default query delta
  https://github.com/fedora-infra/datagrepper/pull/233

0.9.6
=====

Pull Requests

- Drop python2
  https://github.com/fedora-infra/datagrepper/pull/232
  https://github.com/fedora-infra/datagrepper/pull/231
- Add a configuration option to set a default query delta
  https://github.com/fedora-infra/datagrepper/pull/230
- Remove fedmenu
  https://github.com/fedora-infra/datagrepper/pull/227

0.9.5
=====

Pull Requests

- #210, Merge pull request #210 from abitrolly/patch-1
  https://github.com/fedora-infra/datagrepper/pull/210
- #213, Merge pull request #213 from mikebonnet/request-txns
  https://github.com/fedora-infra/datagrepper/pull/213
- #214, Merge pull request #214 from mikebonnet/python3
  https://github.com/fedora-infra/datagrepper/pull/214

Commits

- 7ab64fab3 0.9.4
  https://github.com/fedora-infra/datagrepper/commit/7ab64fab3
- cdcecf841 Fix broken link to fedmsg list of topics
  https://github.com/fedora-infra/datagrepper/commit/cdcecf841
- bc46a1f4c add transaction handling
  https://github.com/fedora-infra/datagrepper/commit/bc46a1f4c
- 2a923f03b minor tweaks to enable datagrepper to run under Python 3
  https://github.com/fedora-infra/datagrepper/commit/2a923f03b
- acdfe10cb remove dangling comment closure
  https://github.com/fedora-infra/datagrepper/commit/acdfe10cb
- a5f34c15e 0.9.4
  https://github.com/fedora-infra/datagrepper/commit/a5f34c15e

0.9.4
=====

Pull Requests

-                   #207, Merge pull request #207 from fedora-infra/pesky-error-handling
  https://github.com/fedora-infra/datagrepper/pull/207

Commits

- 71d8ef88a Fix two bugs.
  https://github.com/fedora-infra/datagrepper/commit/71d8ef88a

0.9.3
=====

Resolving git branch merge conflicts.

0.9.2
=====

Pull Requests

- Fix a 500 error when using "contains" #204, Merge pull request #204 from fedora-infra/fix-500
  https://github.com/fedora-infra/datagrepper/pull/204

Commits

- 9ed123c26 Fix 500 error in "contains" queries.
  https://github.com/fedora-infra/datagrepper/commit/9ed123c26
- 741c8d0e7 Remove unused imports.
  https://github.com/fedora-infra/datagrepper/commit/741c8d0e7
- 488fad49a Some pep8 cleanup.
  https://github.com/fedora-infra/datagrepper/commit/488fad49a
- e2fea1c2f Should always use UTC.
  https://github.com/fedora-infra/datagrepper/commit/e2fea1c2f
- 9add974ad .gitignore for .eggs/
  https://github.com/fedora-infra/datagrepper/commit/9add974ad

0.9.1
=====

Resolve merge conflict in 0.9.0 release.

0.9.0
=====

Pull Requests

-                   #198, Merge pull request #198 from fedora-infra/nopy26
  https://github.com/fedora-infra/datagrepper/pull/198
-                   #200, Merge pull request #200 from jflory7/change/improve-docs
  https://github.com/fedora-infra/datagrepper/pull/200
-                   #203, Merge pull request #203 from mikebonnet/cors-lite
  https://github.com/fedora-infra/datagrepper/pull/203

Commits

- d19f4ee6d Require a recentish start if contains is used
  https://github.com/fedora-infra/datagrepper/commit/d19f4ee6d
- 7040d8239 Also require topic or category
  https://github.com/fedora-infra/datagrepper/commit/7040d8239
- 4dd5b5eac SQLAlchemy no longer supports py2.6, drop the tests on it
  https://github.com/fedora-infra/datagrepper/commit/4dd5b5eac
- 83469ea04 Rewrite documentation to improve readability
  https://github.com/fedora-infra/datagrepper/commit/83469ea04
- 7b3e6acc3 Add test script for testing reST doc generation
  https://github.com/fedora-infra/datagrepper/commit/7b3e6acc3
- 76fd54f2f Update Sphinx extensions, settings; minor docs reformatting
  https://github.com/fedora-infra/datagrepper/commit/76fd54f2f
- 85901d0d6 Add virtualenvs to .gitignore
  https://github.com/fedora-infra/datagrepper/commit/85901d0d6
- af6180989 a very simple CORS implementation
  https://github.com/fedora-infra/datagrepper/commit/af6180989

0.8.0
=====

Pull Requests

- (@ryanlerch)      #177, Update to new Fedora Bootstrap
  https://github.com/fedora-infra/datagrepper/pull/177
- (@cydrobolt)      #180, POST requests are not allowed
  https://github.com/fedora-infra/datagrepper/pull/180
- (@jeremycline)    #184, Update requirements.txt for current dependencies
  https://github.com/fedora-infra/datagrepper/pull/184
- (@rowright)       #187, added UTC to the raw page
  https://github.com/fedora-infra/datagrepper/pull/187
- (@ralphbean)      #188, When people click on the feed, send them to a more gentle query.
  https://github.com/fedora-infra/datagrepper/pull/188
- (@ralphbean)      #193, Make the docs path configurable.
  https://github.com/fedora-infra/datagrepper/pull/193
- (@ralphbean)      #192, Make the Content-Security-Policy configurable.
  https://github.com/fedora-infra/datagrepper/pull/192
- (@ralphbean)      #191, Be nice in case there's a 500 error in flight.
  https://github.com/fedora-infra/datagrepper/pull/191
- (@ralphbean)      #194, Remove an unused link.
  https://github.com/fedora-infra/datagrepper/pull/194
- (@ralphbean)      #195, Make some aspects of the datagrepper UI themeable.
  https://github.com/fedora-infra/datagrepper/pull/195

Commits

- 2015443af swapped over to use fedorabootstrap 1.0
  https://github.com/fedora-infra/datagrepper/commit/2015443af
- 2d8238ac2 ad images and change templates to work with the new fedorabootstrap
  https://github.com/fedora-infra/datagrepper/commit/2d8238ac2
- f1a05c27e removed pull-right class to stop gap appearing
  https://github.com/fedora-infra/datagrepper/commit/f1a05c27e
- 35e53eef5 added font imports to feed page
  https://github.com/fedora-infra/datagrepper/commit/35e53eef5
- 70c64e6e4 made the rows on the feed page thinner
  https://github.com/fedora-infra/datagrepper/commit/70c64e6e4
- 8339f4069 fixed the messages pending button at top of page
  https://github.com/fedora-infra/datagrepper/commit/8339f4069
- 46313f88c make pending msg button hidden on load
  https://github.com/fedora-infra/datagrepper/commit/46313f88c
- 36ec89049 made pending msg button hide properly and fix autoscroll
  https://github.com/fedora-infra/datagrepper/commit/36ec89049
- d5caf0131 made the json appear at the bottom again on the raw display
  https://github.com/fedora-infra/datagrepper/commit/d5caf0131
- 855fd11ea removed old fonts
  https://github.com/fedora-infra/datagrepper/commit/855fd11ea
- 955be6080 added new fonts instead of using external cdn
  https://github.com/fedora-infra/datagrepper/commit/955be6080
- b021034e7 POST requests are not allowed
  https://github.com/fedora-infra/datagrepper/commit/b021034e7
- 5d2eaa529 Update requirements.txt for current dependencies
  https://github.com/fedora-infra/datagrepper/commit/5d2eaa529
- 8ffcca4f4 added UTC to the raw page
  https://github.com/fedora-infra/datagrepper/commit/8ffcca4f4
- 2f8911ab3 When people click on the feed, send them to a more gentle query.
  https://github.com/fedora-infra/datagrepper/commit/2f8911ab3
- 6ddf3e9e9 Be nice in case there's a 500 error in flight.
  https://github.com/fedora-infra/datagrepper/commit/6ddf3e9e9
- 09afabfbf Make the Content-Security-Policy configurable.
  https://github.com/fedora-infra/datagrepper/commit/09afabfbf
- 829db4bef Make the docs path configurable.
  https://github.com/fedora-infra/datagrepper/commit/829db4bef
- 587b64c94 Remove an unused link.
  https://github.com/fedora-infra/datagrepper/commit/587b64c94
- ce866f3de Make some aspects of the datagrepper UI themeable.
  https://github.com/fedora-infra/datagrepper/commit/ce866f3de

0.7.1
=====

Commits

- fb52f6908 Typofix.
  https://github.com/fedora-infra/datagrepper/commit/fb52f6908

0.7.0
=====

Notably, the /topics endpoint (which never worked) has been removed in
this release.


Pull Requests

- (@ralphbean)      #166, Be more explicit with Content-Security-Policy.
  https://github.com/fedora-infra/datagrepper/pull/166
- (@ralphbean)      #167, Make the websocket configurable.
  https://github.com/fedora-infra/datagrepper/pull/167
- (@ralphbean)      #168, Remove /topics endpoint
  https://github.com/fedora-infra/datagrepper/pull/168
- (@ralphbean)      #169, Return JSON with tracebacks for internal server errors.
  https://github.com/fedora-infra/datagrepper/pull/169
- (@ralphbean)      #170, Truncate charts to make things prettier.
  https://github.com/fedora-infra/datagrepper/pull/170
- (@ralphbean)      #174, JSON, not Details.
  https://github.com/fedora-infra/datagrepper/pull/174
- (@pypingou)       #176, Raise a 405 error upon POST queries
  https://github.com/fedora-infra/datagrepper/pull/176

Commits

- 96e109bd9 Be more explicit with Content-Security-Policy.
  https://github.com/fedora-infra/datagrepper/commit/96e109bd9
- 41701ae80 Make the websocket configurable.
  https://github.com/fedora-infra/datagrepper/commit/41701ae80
- 5abbb8d40 Remove /topics endpoint
  https://github.com/fedora-infra/datagrepper/commit/5abbb8d40
- 0abb45e8f Return JSON with tracebacks for internal server errors.
  https://github.com/fedora-infra/datagrepper/commit/0abb45e8f
- 073e5493c Truncate charts to make things prettier.
  https://github.com/fedora-infra/datagrepper/commit/073e5493c
- df1ae1e69 JSON, not Details.
  https://github.com/fedora-infra/datagrepper/commit/df1ae1e69
- ccdac3445 Raise a 405 error upon POST queries
  https://github.com/fedora-infra/datagrepper/commit/ccdac3445
Changelog
=========

0.6.0
=====

- Log exceptions here. `1bc16dfc3 <https://github.com/fedora-infra/datagrepper/commit/1bc16dfc34b074f42778df2bdb481e2e3e84a351>`_
- Remove dataquery stuff `b0ef34324 <https://github.com/fedora-infra/datagrepper/commit/b0ef34324bf643c755b7c5ac3630b8d0ffc7f0b8>`_
- Merge pull request #158 from fedora-infra/feature/remove-dataquery `1f1b78afd <https://github.com/fedora-infra/datagrepper/commit/1f1b78afd311fbe9f97bde1f1a0912288337c760>`_
- Fix squirrely odometer css. `eab9bed0a <https://github.com/fedora-infra/datagrepper/commit/eab9bed0ac16ab1ec4f111506f75b9c42e67f3d2>`_
- Merge pull request #159 from fedora-infra/feature/squirrely-css `0aaa91b71 <https://github.com/fedora-infra/datagrepper/commit/0aaa91b71117bcac94a134b757bc454c4124329d>`_
- The api changed here and we need to adapt. `c264ead90 <https://github.com/fedora-infra/datagrepper/commit/c264ead902f9a8f4c11bf880ac83a8e3ce068bfc>`_
- Merge pull request #163 from fedora-infra/feature/api-changes `2a0a1f0d9 <https://github.com/fedora-infra/datagrepper/commit/2a0a1f0d92b1025bd832f9b7d38406ba01602a4f>`_
- Don't show the loading widget on the single-message page. `72cb18a75 <https://github.com/fedora-infra/datagrepper/commit/72cb18a753cbe66781f9bfd04d2b868a63bd2535>`_
- Show and hide the loading widget the way it was originally intended. `47d127aaf <https://github.com/fedora-infra/datagrepper/commit/47d127aaf3dfbeccc0b77a61967d74ff9d5594ee>`_
- Stop the autoscroll chain once we reach the last page of data. `ac02b145b <https://github.com/fedora-infra/datagrepper/commit/ac02b145b83e59d2d32743ad4351aa77fd1d632f>`_
- Add fedmenu. `a7a128bc2 <https://github.com/fedora-infra/datagrepper/commit/a7a128bc252e7e3437de83b1ffc2551f50ee82a8>`_
- Merge pull request #164 from fedora-infra/feature/loading-widget `141f8f12c <https://github.com/fedora-infra/datagrepper/commit/141f8f12c0623814b787d6ae6e66322d7d896f27>`_
- Merge pull request #165 from fedora-infra/feature/fedmenu `b253c5030 <https://github.com/fedora-infra/datagrepper/commit/b253c503000bb7a0f81776f596d62a50d980ea94>`_

0.5.1
=====

- Hide charts for now. `f7cc99859 <https://github.com/fedora-infra/datagrepper/commit/f7cc99859e7e4b313021e70eeabf810a73a25b5e>`_
- Merge pull request #153 from fedora-infra/feature/hide-charts-for-now `116ec2a56 <https://github.com/fedora-infra/datagrepper/commit/116ec2a56ad0fe86ee2660ea8e7bebfe1581fca4>`_

0.5.0
=====

- Link topic to topic filter on raw page `e6dfe37e5 <https://github.com/fedora-infra/datagrepper/commit/e6dfe37e5e5feb894b9a9c7a90e04b32a7678eba>`_
- Merge pull request #148 from sayanchowdhury/hyperlink-topics `fbe0c1af5 <https://github.com/fedora-infra/datagrepper/commit/fbe0c1af518513e2f689f9325ff05b420a124c65>`_
- First draft of dataviewer. `1abeabd41 <https://github.com/fedora-infra/datagrepper/commit/1abeabd4139523efdbff98a0883dc2b7a4a7d8f6>`_
- Allow different chart types and different styles. `1031a0d77 <https://github.com/fedora-infra/datagrepper/commit/1031a0d7783d5c007b388a849533f314e554f0e6>`_
- lots more options. `87663ab88 <https://github.com/fedora-infra/datagrepper/commit/87663ab88f3f6996034ea4461b7d6b83991e3dcc>`_
- New req. `9bac15dd5 <https://github.com/fedora-infra/datagrepper/commit/9bac15dd59e736dcb557002bf32ae70ae046df53>`_
- First draft of docs. `f041bbb87 <https://github.com/fedora-infra/datagrepper/commit/f041bbb874b3cac3516da87e5997134ceb2d86fd>`_
- Add more example images. `bbafaf97e <https://github.com/fedora-infra/datagrepper/commit/bbafaf97eeb7ead212dc66ac239cac4710038477>`_
- Undo fedmsg.d silliness for #149. `efd308d26 <https://github.com/fedora-infra/datagrepper/commit/efd308d26d02bcc0e7332a540843e17c4d3915be>`_
- Merge pull request #149 from fedora-infra/feature/dataviewer `02322579c <https://github.com/fedora-infra/datagrepper/commit/02322579c5486419fcbc44d4a8ffad5291f32ddf>`_
- Fix README for the xzcat command `8b4eda7f3 <https://github.com/fedora-infra/datagrepper/commit/8b4eda7f3911e06beeedc93d8d429329c19fe3e9>`_
- Use new fedmsg.meta.conglomerate features. `dca29fadf <https://github.com/fedora-infra/datagrepper/commit/dca29fadf92bab9ec821c21cda3d2ed04b94029b>`_
- Get conglomerate stuff working with the embeddable widget too. `6e38c806d <https://github.com/fedora-infra/datagrepper/commit/6e38c806dc89da51eb7f866ea1eba1988776009a>`_
- Quote consistency. `d83201f7c <https://github.com/fedora-infra/datagrepper/commit/d83201f7cbda6ee94cacac6c5be59a085aa4904c>`_
- Merge pull request #150 from fedora-infra/feature/grouped `86b0e0d95 <https://github.com/fedora-infra/datagrepper/commit/86b0e0d95dc9ed46192dd625d18b105abb0aca9b>`_
- Added a basic version footer to datagrepper templates. The foot is ripped from the fmn.web footer `4104f4486 <https://github.com/fedora-infra/datagrepper/commit/4104f44862b0a81303e2c7abcefc65ed5f4d22e8>`_
- Merge pull request #151 from rossdylan/feature/version_footer `266680683 <https://github.com/fedora-infra/datagrepper/commit/2666806834a2b15765b46170aebc36738de67dad>`_

0.4.2
=====

- Fix relative links. `6ac26604f <https://github.com/fedora-infra/datagrepper/commit/6ac26604fdf7ca1cf28d112f8016e1e96c87b5d8>`_
- Merge pull request #140 from fedora-infra/feature/static-files `aed1bd0fd <https://github.com/fedora-infra/datagrepper/commit/aed1bd0fde1e42c1403b8443fd8b0990340fa18b>`_
- Only show links in the widget if they're not null. `dd282e687 <https://github.com/fedora-infra/datagrepper/commit/dd282e6871fdefb71a01c30f8ccb131e9e1c0c3c>`_
- Only show links in the raw template if they're not null. `c91efb5bc <https://github.com/fedora-infra/datagrepper/commit/c91efb5bc778659a845c46d5abc6049df3340d14>`_
- Merge pull request #141 from fedora-infra/feature/fix-null-links `924ae006a <https://github.com/fedora-infra/datagrepper/commit/924ae006ade6d8965e2f23ceecb9dd1b31743825>`_
- Patch out flask-sqlalchemy. `3d332a96f <https://github.com/fedora-infra/datagrepper/commit/3d332a96f30675233f48b504a67c73a48e1f7cd2>`_

0.4.1
=====

- Update README.rst `b17d8dde7 <https://github.com/fedora-infra/datagrepper/commit/b17d8dde75bbacec6cea275cd1c0a11970e2d778>`_
- Update README.rst `ffac3f811 <https://github.com/fedora-infra/datagrepper/commit/ffac3f81182847d45938638469bac94ac15db571>`_
- Update README.rst `8404c70c0 <https://github.com/fedora-infra/datagrepper/commit/8404c70c038c82a0e6377dc20cbbf636d1e2f400>`_
- Update README.rst `752b912f7 <https://github.com/fedora-infra/datagrepper/commit/752b912f70475fa27b9615e4d7f56877abe6418c>`_
- Use a pygments style that exists on old, old el6. `d671c8d27 <https://github.com/fedora-infra/datagrepper/commit/d671c8d274e7ff1c4c882ce92b9b7e001e387312>`_
- remove unused css. `60134c1b0 <https://github.com/fedora-infra/datagrepper/commit/60134c1b0f09bdd52fe8d9f34dbd7645400309fe>`_
- Merge pull request #131 from fedora-infra/feature/old-pygments `57ca7245f <https://github.com/fedora-infra/datagrepper/commit/57ca7245f20a7db331715d36583686e75102ad2e>`_
- Merge pull request #130 from haseebgit/develop `eef1af9a4 <https://github.com/fedora-infra/datagrepper/commit/eef1af9a40fdd446b8d07f276eb0109ae63f8121>`_
- Require an id on the widget script tag to avoid assuming it is last on the page. `5292d5087 <https://github.com/fedora-infra/datagrepper/commit/5292d50871ff36c4ec0788c7d79eafb6649aa699>`_
- Update the docs to include the script id `6596b10ea <https://github.com/fedora-infra/datagrepper/commit/6596b10ea0182e5cdae18ae6262380debaabc239>`_
- Update the docs to show how you can customize the widget style `6ef4603c7 <https://github.com/fedora-infra/datagrepper/commit/6ef4603c7419a35e634994d6e0e82043f100c957>`_
- Use http with "--json" everywhere `808caee4e <https://github.com/fedora-infra/datagrepper/commit/808caee4e1028336813b5ab2580652dd97a6e7b5>`_
- Also, convert /raw/ to /raw... `e77048b30 <https://github.com/fedora-infra/datagrepper/commit/e77048b302c6f08f884872b40b7d6fb72f674755>`_
- Typofix. `caeb2ad34 <https://github.com/fedora-infra/datagrepper/commit/caeb2ad3484212a6a3a32ede567ebdbc7a732821>`_
- Revert the "--json" advice. `82a89a266 <https://github.com/fedora-infra/datagrepper/commit/82a89a266b73b3c847dbb4c9925b2be13787a34f>`_
- Fix header handling. `ee0f3e69b <https://github.com/fedora-infra/datagrepper/commit/ee0f3e69b714ab87e4a3854e94deba938bb5a811>`_
- Merge pull request #133 from fedora-infra/feature/widget-id `96ded5554 <https://github.com/fedora-infra/datagrepper/commit/96ded5554ca9b11d43ae1462091f5c68d364a0d3>`_
- Merge pull request #134 from fedora-infra/feature/httpie-with-json `ed26cfc20 <https://github.com/fedora-infra/datagrepper/commit/ed26cfc201fcf749666694cae660be91baae032d>`_
- Make the msg_id endpoint support jsonp just like the raw endpoint. `c9d540812 <https://github.com/fedora-infra/datagrepper/commit/c9d5408120128b9a64368c6fe4f995ef53623afb>`_
- Merge pull request #135 from fedora-infra/feature/jsonp-for-msg_id `f6f89acf1 <https://github.com/fedora-infra/datagrepper/commit/f6f89acf1329a002218f7d28eb5621873bd9fd30>`_
- Point at the new db dump.  Thanks @nirik! `3e15e8d38 <https://github.com/fedora-infra/datagrepper/commit/3e15e8d38b60e31ec9cb5ec2c1989ec45cca90c8>`_
- Use latest bootstrap and fix style on the docs pages. `668c77656 <https://github.com/fedora-infra/datagrepper/commit/668c7765607a81b7a32609da7d52fe6bced7ca67>`_
- Fix "raw page" css to be a little more sane, especially on mobile. `524f17d44 <https://github.com/fedora-infra/datagrepper/commit/524f17d44e8633820cf89e4f35ea926db6890c29>`_
- Merge pull request #136 from fedora-infra/feature/mobile-view `1478d00fd <https://github.com/fedora-infra/datagrepper/commit/1478d00fdc4709c2567a44a498dde2d8266a7802>`_
- Autoscrolling on the /raw endpoint. `73ecd9f39 <https://github.com/fedora-infra/datagrepper/commit/73ecd9f393e713464966427fbb69123c11ad7d03>`_
- Remove goofy debugging. `dede0183e <https://github.com/fedora-infra/datagrepper/commit/dede0183e4e6082eea28f6618afb9111760daa19>`_
- Merge pull request #137 from fedora-infra/feature/autoscroll `ddc5e47b5 <https://github.com/fedora-infra/datagrepper/commit/ddc5e47b56fe5186e2393585dc1f1f814bee2f2c>`_
- Set a favicon for the query page. `c30c16328 <https://github.com/fedora-infra/datagrepper/commit/c30c16328657fac19528eb7695c7a1fca9e8e192>`_
- Just say no to javascript. `b0adf9b00 <https://github.com/fedora-infra/datagrepper/commit/b0adf9b007790ba12cf524ec782dec18b4b7316e>`_
- Allow "traditional" multidict. `b766cb870 <https://github.com/fedora-infra/datagrepper/commit/b766cb8703585c09d2dd0214447dc64cf3140960>`_
- Merge pull request #138 from fedora-infra/feature/fix-the-wat `8525498e2 <https://github.com/fedora-infra/datagrepper/commit/8525498e26b9e39c98a1f866ae4b94e6964d6dd0>`_
- Now with websockets! `c78c14d2b <https://github.com/fedora-infra/datagrepper/commit/c78c14d2b4de45eecc1b437cc476962b8cf1f1a4>`_
- Add CSP for websockets. `96d8e649b <https://github.com/fedora-infra/datagrepper/commit/96d8e649bf5a47535fa2bb13c00d34bf2e070df3>`_
- Remove unused css. `fec9d7f34 <https://github.com/fedora-infra/datagrepper/commit/fec9d7f34c8d1a5c5b6b0e65c0dd3a813832c1d0>`_
- Make this title a little more friendly. `d7e4e1abc <https://github.com/fedora-infra/datagrepper/commit/d7e4e1abc6f98212b27411b005386c133b26b73e>`_
- Merge pull request #139 from fedora-infra/feature/websockets `c5803db67 <https://github.com/fedora-infra/datagrepper/commit/c5803db677761b8275fc2620b75efcd061375d79>`_

0.4.0
=====

- If the user is expecting jsonp, there's no way they want html... `c9e8d977f <https://github.com/fedora-infra/datagrepper/commit/c9e8d977fc3c166ccb68a9b4ed9bfa5c5deb49e4>`_
- Fix widget css resources paths. `3129baed8 <https://github.com/fedora-infra/datagrepper/commit/3129baed8c49d0d8e2d0196b75145018b4faec0c>`_
- Move APP_PATH config to the default_config module. `676bdef7a <https://github.com/fedora-infra/datagrepper/commit/676bdef7a43d0362ace984dc32e40bbcea446554>`_
- Merge pull request #122 from fedora-infra/feature/fix-jsonp `609b3caf8 <https://github.com/fedora-infra/datagrepper/commit/609b3caf8e55ca279e17731cb5d99a824b095b35>`_
- Merge pull request #123 from fedora-infra/feature/fix-widget-css `b0fa7940e <https://github.com/fedora-infra/datagrepper/commit/b0fa7940eb7bb7e2c3d1020939589ffe8c7720e8>`_
- Make message count always be an int `03337713b <https://github.com/fedora-infra/datagrepper/commit/03337713b5047ebd34732493ae21d277a1df04ee>`_
- Optimize count_all_messages() `aa1363950 <https://github.com/fedora-infra/datagrepper/commit/aa1363950efcaa291a213aff55b0be7cc4ce0fc1>`_
- Merge pull request #124 from fedora-infra/int-messagecount `c5ea239e7 <https://github.com/fedora-infra/datagrepper/commit/c5ea239e7fcad58d724040c6354afd0661e2dacb>`_
- Merge pull request #125 from fedora-infra/feature/defer-count-query `4df9a49fb <https://github.com/fedora-infra/datagrepper/commit/4df9a49fb5ede12d2459118b2a6058f559ebac2a>`_
- Work the /id/ endpoint `4b57c84e1 <https://github.com/fedora-infra/datagrepper/commit/4b57c84e111a7012400bf9ebdee888f933328505>`_
- Display the message in size extra-large `38403ef6a <https://github.com/fedora-infra/datagrepper/commit/38403ef6a192e2ffa49992143c4a0ffc31f1c9f3>`_
- When linking to the id page, we have the space so go for the largest size `28e64402a <https://github.com/fedora-infra/datagrepper/commit/28e64402a8f5234017a094cac9df3d6c7872b348>`_
- Update docs for extra-large size. `a04ed00a6 <https://github.com/fedora-infra/datagrepper/commit/a04ed00a654b835658e89f46b8c043f8f8728dc3>`_
- Typofix. `5ae033c2a <https://github.com/fedora-infra/datagrepper/commit/5ae033c2aa4b200ff227585e8216c9fbd2c6a71a>`_
- Colorized the json here. `7c6c5231b <https://github.com/fedora-infra/datagrepper/commit/7c6c5231b6e125480b753fa086d94134fa15c7d0>`_
- Add extra-large to the message_card util. `58d877a45 <https://github.com/fedora-infra/datagrepper/commit/58d877a4530b84603c2fc2e97e105dfb348c84ff>`_
- Make "desc" the default ordering to save on typing. `cb33da116 <https://github.com/fedora-infra/datagrepper/commit/cb33da116566e25fe3632cab2d2d1e150e831372>`_
- Merge pull request #128 from fedora-infra/feature/default-is-desc `92fdb8f4f <https://github.com/fedora-infra/datagrepper/commit/92fdb8f4fcc9241b0f35414ccf14d981f93a8e51>`_
- Merge pull request #127 from fedora-infra/feature/msg_in_card `934be9a09 <https://github.com/fedora-infra/datagrepper/commit/934be9a091c3c6299a4505e31dc36a85c29a6cb2>`_
- PEP8/cosmetic. `834dad9a0 <https://github.com/fedora-infra/datagrepper/commit/834dad9a08c48c3e7626d223c1022de0348ad672>`_
- Merge pull request #129 from fedora-infra/feature/pep8 `f6a93ede0 <https://github.com/fedora-infra/datagrepper/commit/f6a93ede0becb51825751a675321e298a481cd98>`_

0.3.3
=====

- Merge pull request #106 from charulagrl/fedpkg `b16756c2c <https://github.com/fedora-infra/datagrepper/commit/b16756c2cf2f65ff1f388aaa5a98b38eab081bbd>`_
- added div and span tag for images and details link respectively `c84c05d98 <https://github.com/fedora-infra/datagrepper/commit/c84c05d98a1c608c3c380dde28fdb6de54e31a41>`_
- added definitions for various classes `f8d87b0f9 <https://github.com/fedora-infra/datagrepper/commit/f8d87b0f9bd6882652d69baf85f00f43bcc80dd8>`_
- changed the layout of message-card `71a83df95 <https://github.com/fedora-infra/datagrepper/commit/71a83df95c96be9fe4143fea271acce6fc2ce978>`_
- includes raw.css file `5c9ef2eb9 <https://github.com/fedora-infra/datagrepper/commit/5c9ef2eb993e86ef528f5330d4a675045401e0d5>`_
- removed unnecessary curly brackets from heading Datagrepper Messages `ca460a723 <https://github.com/fedora-infra/datagrepper/commit/ca460a7232cb1898654f1ceaedfa4d2116e5328b>`_
- Merge pull request #107 from charulagrl/fedpkg `32c0a8416 <https://github.com/fedora-infra/datagrepper/commit/32c0a84168328c1f4974bf15bf55588aecdfab67>`_
- Convert the msg timestamp into a datetime object to make the date available in the card `304c91f45 <https://github.com/fedora-infra/datagrepper/commit/304c91f45c580b7378301c43f17c26389ccc6008>`_
- Small HTML fixes, add the date to the card and fix link to the individual message by its id `09c87af56 <https://github.com/fedora-infra/datagrepper/commit/09c87af56c6b266ad3ab88e3d7e3acde4d56d279>`_
- Make sure the dates are converted in UTC `dd472ff33 <https://github.com/fedora-infra/datagrepper/commit/dd472ff3313972229404c7172a63b64396479fa0>`_
- Use arrow to parse the date from the raw_message `007981f89 <https://github.com/fedora-infra/datagrepper/commit/007981f897a139ca57ff4c3f82320a0af5a466d2>`_
- Display the date in full if size == 'large' otherwise just the relative date provided by arrow `ff049fcbc <https://github.com/fedora-infra/datagrepper/commit/ff049fcbca149fd5f2dda265f4367b277fd9dba7>`_
- Merge pull request #105 from fedora-infra/add_dates `384ff89ac <https://github.com/fedora-infra/datagrepper/commit/384ff89ac0bf15ae1dfe5e041012e0eaaf642271>`_
- changed the css for datetime `1c5b5ed76 <https://github.com/fedora-infra/datagrepper/commit/1c5b5ed76e2806a15e310c34b33fd74ee8af2a0b>`_
- changed the position of datetime element `3fb180616 <https://github.com/fedora-infra/datagrepper/commit/3fb1806166e37db28f9621bbd184e0d250118a71>`_
- Merge pull request #108 from charulagrl/develop `68142cf5f <https://github.com/fedora-infra/datagrepper/commit/68142cf5f7af431d23024ecbc6cc4a1be2f2c925>`_
- Optimize frontpage for #101. `54b077e1f <https://github.com/fedora-infra/datagrepper/commit/54b077e1fe2788d1ec76df46fc032004c5cf8546>`_
- Add jquery to avoid 1s delay before initializing odometer. `2b71d071d <https://github.com/fedora-infra/datagrepper/commit/2b71d071d097af368eb01f03c25911889d0145b7>`_
- Actually, we can just set the value on the server. `ecde1ff21 <https://github.com/fedora-infra/datagrepper/commit/ecde1ff214adf2ef1163415e7b60fd5673e23b4c>`_
- No more "Arimo" google font.  Fixes #103 `7dc66bea7 <https://github.com/fedora-infra/datagrepper/commit/7dc66bea7967da4d74ceed9f792e0a01e19951e9>`_
- Merge pull request #110 from fedora-infra/feature/count-from-zero `fe0a0a7a0 <https://github.com/fedora-infra/datagrepper/commit/fe0a0a7a0044de6ab56588bee124de7bb08135d7>`_
- Break that optimization conditional out into a utility function. `4b9a4ab5a <https://github.com/fedora-infra/datagrepper/commit/4b9a4ab5a378e1c768db5a039e121d4efa83bf29>`_
- Merge pull request #109 from fedora-infra/feature/optimize-frontpage `056dae5eb <https://github.com/fedora-infra/datagrepper/commit/056dae5eb85f188a43e4e2981e876d453ac8e0e5>`_
- Merge pull request #111 from fedora-infra/feature/font-fixing `e78a71ebb <https://github.com/fedora-infra/datagrepper/commit/e78a71ebb776b878bf6fc887deab1a20949cd9cc>`_
- Update docs to point at the latest snapshot. `67d3ac220 <https://github.com/fedora-infra/datagrepper/commit/67d3ac220151d247556f50927dffb6458f6273d1>`_
- Merge pull request #112 from fedora-infra/feature/latest-snapshot `25afc011b <https://github.com/fedora-infra/datagrepper/commit/25afc011b18b316a57848ce17b90747843e619c3>`_
- Update README.rst `a6ff96a36 <https://github.com/fedora-infra/datagrepper/commit/a6ff96a36019c8faf030b6c608955ac80a8a2347>`_
- removed the instruction added before `2b2d5eb42 <https://github.com/fedora-infra/datagrepper/commit/2b2d5eb42c301c0617acdbe914e1255bda0fb42b>`_
- added fedmsg_meta_fedora_infrastructure `19a07ff17 <https://github.com/fedora-infra/datagrepper/commit/19a07ff17e10aea518e367dd337ba7b39137ec73>`_
- Update the documentation `d8c9715e2 <https://github.com/fedora-infra/datagrepper/commit/d8c9715e20c345927ae5e80ae0f475f132101bfa>`_
- Merge pull request #113 from charulagrl/patch-1 `98ce4bb1e <https://github.com/fedora-infra/datagrepper/commit/98ce4bb1ec8cfd47201eb0d1bc8c954c564b58f4>`_
- Merge remote-tracking branch 'upstream/master' into fedpkg `5731277e4 <https://github.com/fedora-infra/datagrepper/commit/5731277e4619660f07c44aca89099c7c5c50d2dd>`_
- changed the width of image `a7be2e399 <https://github.com/fedora-infra/datagrepper/commit/a7be2e3991819059dfd3bf0116471325d6c94ea4>`_
- Update reference.rst `2c6b11544 <https://github.com/fedora-infra/datagrepper/commit/2c6b115449f49d6b90624ed075cffd721f6d82e0>`_
- Update reference.rst `3fcdf22de <https://github.com/fedora-infra/datagrepper/commit/3fcdf22dedac4e85f26ea50c7972f61f0575010e>`_
- Merge pull request #115 from charulagrl/fedpkg `a6ba30815 <https://github.com/fedora-infra/datagrepper/commit/a6ba30815a219ce46e04643622b3c61cfaa8512f>`_
- Update reference.rst `0769068ec <https://github.com/fedora-infra/datagrepper/commit/0769068ecceff16185a2d096dd9cf179114e6112>`_
- Update reference.rst `b0f4706ec <https://github.com/fedora-infra/datagrepper/commit/b0f4706ec17e9290461225d07abfbc3365a24c8b>`_
- Merge pull request #116 from charulagrl/patch-2 `520bf0e93 <https://github.com/fedora-infra/datagrepper/commit/520bf0e9345b96a057b51bd9ba479615cc789d6b>`_
- Check for existance of secondary_icon. `62ec18b67 <https://github.com/fedora-infra/datagrepper/commit/62ec18b67a8d1ee0a116490a3003a91a319ded52>`_
- 0.3.1 `230b4d50a <https://github.com/fedora-infra/datagrepper/commit/230b4d50af2b83625b9cbd828b8255b00c11d4a2>`_
- Also check to make sure the icon is not None. `d991f2a0b <https://github.com/fedora-infra/datagrepper/commit/d991f2a0be5e54a7c3c6a6ae7440b4280d47fae2>`_
- 0.3.2 `a1ad7e228 <https://github.com/fedora-infra/datagrepper/commit/a1ad7e228ec022bb6145890328349f2eb710f38b>`_
- First start of a functional widget. `1fb98a97e <https://github.com/fedora-infra/datagrepper/commit/1fb98a97efe9cfb384e1abe72275cbb131b206fe>`_
- Fixes to query. `519a9cd8e <https://github.com/fedora-infra/datagrepper/commit/519a9cd8e6882dc6ea48e040eb00768c7665eaa6>`_
- Allow users to pass arguments to the js widget query. `58acb1b54 <https://github.com/fedora-infra/datagrepper/commit/58acb1b5462246911f192c317a20b66059ee96c7>`_
- Removed old unused stuff. `5de9b4b7e <https://github.com/fedora-infra/datagrepper/commit/5de9b4b7e3e1249e68a51d9486ca0f699a9f0e53>`_
- Optionally add in css for the embedded widget. `2d4aee9e5 <https://github.com/fedora-infra/datagrepper/commit/2d4aee9e51ea204a6c3bd8548de83fd0a00228ba>`_
- Add a docs page for the embeddable widget. `2e3e08f4a <https://github.com/fedora-infra/datagrepper/commit/2e3e08f4a872ac8ab0610a80455bd3ce86c49df7>`_
- Reformat meta example list and add the new 'date' field. `8aac1e695 <https://github.com/fedora-infra/datagrepper/commit/8aac1e695c914d71e21c23024e1fce546f4feefa>`_
- Merge pull request #117 from fedora-infra/feature/embeddable-js-widget `a7c99c36c <https://github.com/fedora-infra/datagrepper/commit/a7c99c36c3f04fa1f42241204e058e60734a311d>`_
- Add negative filters. `8a153c169 <https://github.com/fedora-infra/datagrepper/commit/8a153c1698e598161a41d02951ce0eb3717d00fc>`_
- Update docs with new negative filters. `2814c1990 <https://github.com/fedora-infra/datagrepper/commit/2814c19907105c52617a84be3d0bea4d2061339e>`_
- Merge pull request #120 from fedora-infra/feature/negative-filters `6826f440e <https://github.com/fedora-infra/datagrepper/commit/6826f440e713c813f6cc206e29fb2aeadeef2d0b>`_
- Add possibility to query the database with a keyword and retrieve all messages having it `601642197 <https://github.com/fedora-infra/datagrepper/commit/6016421972817377221f30b8dd5e3b6641a449ba>`_
- Merge pull request #121 from fedora-infra/feature/contains `9e2d2ea40 <https://github.com/fedora-infra/datagrepper/commit/9e2d2ea4080c62e98476aa6bfc2bc7076d3948ef>`_

0.3.0
=====

- Merge branch 'master' into develop `2af554420 <https://github.com/fedora-infra/datagrepper/commit/2af5544202ee564634cc1e5345b5c76cfccb3393>`_
- Changes made in 'raw' url i.e. it returns the actual content except if content-type is html `1eb9cef53 <https://github.com/fedora-infra/datagrepper/commit/1eb9cef53baaaf5a60f932f711bfc1420a0d9966>`_
- removed a extra whitespace `d2167fd95 <https://github.com/fedora-infra/datagrepper/commit/d2167fd95e8563d76c6c3aa5b7f64d860cfd839c>`_
- used request_wants_html to get content according to mimetypes `3f05b41c5 <https://github.com/fedora-infra/datagrepper/commit/3f05b41c5ab533fb111f9e494c44a3c5f65085b8>`_
- changed request_wants_json to request_wants_html `b233e8c99 <https://github.com/fedora-infra/datagrepper/commit/b233e8c996ba4792ae31acec26c8c750363df035>`_
- Merge pull request #80 from charulagrl/develop `763f4db40 <https://github.com/fedora-infra/datagrepper/commit/763f4db4009774f88e764622f9fc8c8a8a751150>`_
- return html content if accept header is 'text/html' `30ebb44d6 <https://github.com/fedora-infra/datagrepper/commit/30ebb44d63938f107e6508a3a456c6df23968ef4>`_
- html file to render raw messages in a beautiful way `d2d105251 <https://github.com/fedora-infra/datagrepper/commit/d2d105251e36d6ca1acbb8fcec664ab8a9722b57>`_
- using fedmsg.meta to return the message in human readable form `3c312f747 <https://github.com/fedora-infra/datagrepper/commit/3c312f747fd22a705c05e93579b3050d0cc29c0c>`_
- looping over the entire messageList and calling fedmsg.meta to display all the messages `4b9b85c4a <https://github.com/fedora-infra/datagrepper/commit/4b9b85c4acd543a134deb7a645799c2a6781e126>`_
- html file to render raw messages(return by fedmsg.meta) `c220f4f14 <https://github.com/fedora-infra/datagrepper/commit/c220f4f14400fa0eceddea833c5d9d69f32a6284>`_
- convert raw_message into icon, link and title. Also, icon is clickable i.e. link opens up when icon is clicked. `4134af8bf <https://github.com/fedora-infra/datagrepper/commit/4134af8bf1b058b3784468eabb5bb63eddc91b39>`_
- html file to render icon, link and title. `d8c154cc9 <https://github.com/fedora-infra/datagrepper/commit/d8c154cc993415065baec70075f93bab9c4e3871>`_
- Merge pull request #81 from charulagrl/develop `be59d09c1 <https://github.com/fedora-infra/datagrepper/commit/be59d09c1e9e055aa9b362349c545ca72b4eee2c>`_
- returns a list of dictionary where each dictionary has icon, link, title and secondary_icon. `d27aac949 <https://github.com/fedora-infra/datagrepper/commit/d27aac949d3c08e15f573fc8e67f654df1d18c71>`_
- html file that renders icon, link, title and secondary_icon `fd2888a17 <https://github.com/fedora-infra/datagrepper/commit/fd2888a1725c16890a784d7e344a112ba615a475>`_
- returns subtitle in addition to icon, title, secondary_icon and link `de8b8e2db <https://github.com/fedora-infra/datagrepper/commit/de8b8e2db453346a7a1bbb05ad2fd3f4b2430c99>`_
- html file to render subtitle, title, icon, secondary_icon, link `ee34fed63 <https://github.com/fedora-infra/datagrepper/commit/ee34fed63c582cc234d1fa5f5df84e4f8d00c8c0>`_
- html to render messages by their id `37d9fa080 <https://github.com/fedora-infra/datagrepper/commit/37d9fa08067d0030f02a09fedc788a9674836a4c>`_
- /id endpoint return html if visited with a browser and JSON otherwise `27a13a6dc <https://github.com/fedora-infra/datagrepper/commit/27a13a6dc5b384ef32f16c514444f9ac31a9da4f>`_
- used fedmsg.meta modules `ea2b47a38 <https://github.com/fedora-infra/datagrepper/commit/ea2b47a38dcda9c088e1cb1f9aa9e6390f84aaff>`_
- html to render a msg by its id `0dbf56cfa <https://github.com/fedora-infra/datagrepper/commit/0dbf56cfa5f9bb2cfe6c28fd4b58cd7f23862c9a>`_
- added message_card module in util.py `4b46a4e92 <https://github.com/fedora-infra/datagrepper/commit/4b46a4e920db5f860a97128dc27e6633259fe92c>`_
- added message_card module `dfd3d3065 <https://github.com/fedora-infra/datagrepper/commit/dfd3d30658ab3e70eead7c77e34fc4718abee62e>`_
- made changes so that it render both id and raw endpoints `953cee898 <https://github.com/fedora-infra/datagrepper/commit/953cee89893ddd42ce685709a9fd16e8103e7785>`_
- Merge pull request #88 from charulagrl/develop `d5482c4ec <https://github.com/fedora-infra/datagrepper/commit/d5482c4ec2b817191750b38669b4669e00f124f3>`_
- An updated db snapshot for development. `b0400d855 <https://github.com/fedora-infra/datagrepper/commit/b0400d8556ddab4adb88a12be30aad0c829bd441>`_
- Merge pull request #89 from fedora-infra/feature/updated-snapshot2 `8a40633f5 <https://github.com/fedora-infra/datagrepper/commit/8a40633f57675c0ade8079479ce9d7dfc2b0da78>`_
- Merge pull request #90 from charulagrl/develop `f2d4a5678 <https://github.com/fedora-infra/datagrepper/commit/f2d4a567893afc8cfeea4fe6c5986fc91059790d>`_
- removed the unwanted trailing spaces `941f06165 <https://github.com/fedora-infra/datagrepper/commit/941f06165302b0cc2b86577373a627f85828988b>`_
- corrected the indentation `863b482ea <https://github.com/fedora-infra/datagrepper/commit/863b482ea787a5c747aacf3928cf9cf98d4e5316>`_
- return cards according to their size `a526b56a5 <https://github.com/fedora-infra/datagrepper/commit/a526b56a55f6e2222f0cb955087f72364a4e2c34>`_
- message_card adds content according to their size `4502d7c7e <https://github.com/fedora-infra/datagrepper/commit/4502d7c7e31631bb50d3563043cbeb036834a9b1>`_
- html file to render message cards by their size `9209e3323 <https://github.com/fedora-infra/datagrepper/commit/9209e332358f7dc74c0f2719d5bfd48409b3f505>`_
- Merge branch 'develop' of github.com:charulagrl/datagrepper into develop `a1fc5957a <https://github.com/fedora-infra/datagrepper/commit/a1fc5957a96553d64d5cd0b39862649f8e2bca27>`_
- Merge pull request #91 from charulagrl/develop `6279bbed5 <https://github.com/fedora-infra/datagrepper/commit/6279bbed51c91d1e403153f0874b8e03e3be9467>`_
- cards now have configurable 'chrome' `6990521f7 <https://github.com/fedora-infra/datagrepper/commit/6990521f77bf2f79e6941177e28297a00660e649>`_
- separated the jinja code `5bbc877cf <https://github.com/fedora-infra/datagrepper/commit/5bbc877cf304533672d4916f28f8af37b249db74>`_
- html boilerplate `279639a8e <https://github.com/fedora-infra/datagrepper/commit/279639a8e2d04c50d85da8c80cd2945ef5c7a2d0>`_
- Merge pull request #93 from charulagrl/develop `de0f3aaff <https://github.com/fedora-infra/datagrepper/commit/de0f3aaffcc2fae9974ac7a9288efce0b1085f34>`_
- adding msg_id field to the message dictionary `3081e83e7 <https://github.com/fedora-infra/datagrepper/commit/3081e83e752152f07f9ed885cfc3701016daed81>`_
- contains a link back to the /id endpoint for messages whose msg_id != None `dfd829980 <https://github.com/fedora-infra/datagrepper/commit/dfd82998096a6ba76022c2dacdbc51d07d17542c>`_
- checks if card comes from /raw url or /id url `fa4902f88 <https://github.com/fedora-infra/datagrepper/commit/fa4902f88fbff2efd3875d9d4ef6ea8f9deb23ed>`_
- contains a Go Back link if card is from /raw url `9499df58d <https://github.com/fedora-infra/datagrepper/commit/9499df58d73ba4bc999a07341481907d16b6b877>`_
- Merge pull request #94 from charulagrl/develop `b02391ea9 <https://github.com/fedora-infra/datagrepper/commit/b02391ea93c2677ec52ec4eb1cbb657b2d6ff24d>`_
- /id endpoint can accept meta arguments `eead053bf <https://github.com/fedora-infra/datagrepper/commit/eead053bf56264e334e1073eff1c71d4f865938d>`_
- removed common codes from msg_id and raw function `6aef53a16 <https://github.com/fedora-infra/datagrepper/commit/6aef53a16f66e9e022c5bd467df9f69fd70484c3>`_
- meta_arguments function consists of the common codes `50c3f656b <https://github.com/fedora-infra/datagrepper/commit/50c3f656b3caf8d6e44cd9f816f516280c46efeb>`_
- Merge pull request #95 from charulagrl/develop `586da5c34 <https://github.com/fedora-infra/datagrepper/commit/586da5c34f643de735b2b624f0f9e7d8c0db1c9d>`_
- Merge branch 'develop' of github.com:fedora-infra/datagrepper into develop `8ac9d21df <https://github.com/fedora-infra/datagrepper/commit/8ac9d21dfba81ea6e88ff7d398729f92b6c5b46b>`_
- added /messagecount endpoint `e86169f5b <https://github.com/fedora-infra/datagrepper/commit/e86169f5b8043a24a4365e80fc9124df461f4a86>`_
- html file to render messagecount `7af735d9c <https://github.com/fedora-infra/datagrepper/commit/7af735d9c2a63b3ced9642ca6ef385a7f80f036d>`_
- Merge branch 'develop' of github.com:charulagrl/datagrepper into develop `a783f00a4 <https://github.com/fedora-infra/datagrepper/commit/a783f00a472c56c5d5d821486881cab961c9bfca>`_
- added messagecount on front page `1aacaa7ad <https://github.com/fedora-infra/datagrepper/commit/1aacaa7ad7e348bd65784a75ec1204feec01a52b>`_
- renders messagecount `5eea4ed65 <https://github.com/fedora-infra/datagrepper/commit/5eea4ed65a0abffe08a2ee8c0dba4b6bea042703>`_
- odometer.js file to render messagecount `a868ef5d2 <https://github.com/fedora-infra/datagrepper/commit/a868ef5d2d5f644378e456dbafdeba81aae6893f>`_
- css file `64aa4a165 <https://github.com/fedora-infra/datagrepper/commit/64aa4a165b746747bfaf6a02039f6fdddedbbc44>`_
- added messagecount on front page `07468aad3 <https://github.com/fedora-infra/datagrepper/commit/07468aad352b02439f1e7486215a640ea89f16ce>`_
- Merge branch 'develop' of github.com:charulagrl/datagrepper into develop `253653b55 <https://github.com/fedora-infra/datagrepper/commit/253653b5500dd851e1bd78de98302c85c8794d50>`_
- Merge pull request #96 from charulagrl/develop `7ddba23ce <https://github.com/fedora-infra/datagrepper/commit/7ddba23ce7371f96fd0c6e457592cd04b86d0047>`_
- /messagecount endpoint returns json dict `1e575b5a3 <https://github.com/fedora-infra/datagrepper/commit/1e575b5a313450f7c9b4d1b9aa9d431cb07b78ef>`_
- /messagecount endpoint returns json dict `3fb9162b6 <https://github.com/fedora-infra/datagrepper/commit/3fb9162b65812ceaeb1a8d9868c5b64c02d0491c>`_
- update the odometer with websockets `38299525e <https://github.com/fedora-infra/datagrepper/commit/38299525eca2de05005c131c8097d969f03fd225>`_
- Merge branch 'develop' of github.com:charulagrl/datagrepper into develop `26dd07e54 <https://github.com/fedora-infra/datagrepper/commit/26dd07e543bcd9c6ada31b8defde83952ef94816>`_
- update messagecount with websockets `3aa6edd7c <https://github.com/fedora-infra/datagrepper/commit/3aa6edd7c64bf8deaec0f9bd8c3eacfcd4bfaa15>`_
- making few corrections `f9423aba2 <https://github.com/fedora-infra/datagrepper/commit/f9423aba2e90a21626b7c414e1c1d2b6c59c9c36>`_
- Merge pull request #98 from charulagrl/develop `09389a7de <https://github.com/fedora-infra/datagrepper/commit/09389a7de5f1a292c90dc322edac9b5b7cf4b119>`_
- Merge branch 'develop' of github.com:fedora-infra/datagrepper into develop `6c3c44582 <https://github.com/fedora-infra/datagrepper/commit/6c3c44582ec095c500b5db6bcc827c04dec7ed7e>`_

0.2.1
=====

- WSGI script needs the same fix as runserver. `19ff2b770 <https://github.com/fedora-infra/datagrepper/commit/19ff2b770027d25b7cbb699ba6901dc26f91915a>`_
- Handle the case where "start" and "end" are None. `181d337a4 <https://github.com/fedora-infra/datagrepper/commit/181d337a43d56f12f9022f550c1df0a0338eb06d>`_
- Merge pull request #44 from fedora-infra/feature/handle-nonetype `ef658eb0a <https://github.com/fedora-infra/datagrepper/commit/ef658eb0a22947b10413e5a0981e845b49986e71>`_
- Fix unexpected indentation that was breaking the rst conversion to html `9105e23e1 <https://github.com/fedora-infra/datagrepper/commit/9105e23e19022c3c4012edd6f729e00e30ef55bf>`_
- Merge pull request #47 from fedora-infra/feature/fix_references_rst `8ad7795a7 <https://github.com/fedora-infra/datagrepper/commit/8ad7795a75adc843e1f8f06ff4db61cb8084b22d>`_
- Merge branch 'master' of github.com:fedora-infra/datagrepper into develop `bce089bc2 <https://github.com/fedora-infra/datagrepper/commit/bce089bc2cc185d498d630c8d24b5127f2f5e5de>`_
- Initial creation of DataQuery obj/module `f6e64dc44 <https://github.com/fedora-infra/datagrepper/commit/f6e64dc44c3389c956b410281a9cb5491cc72276>`_
- PEP 8 fix `ae8febd91 <https://github.com/fedora-infra/datagrepper/commit/ae8febd918d07d5624f1119697b601d72c58a46b>`_
- Merge branch 'develop' of github.com:fedora-infra/datagrepper into feature/submit-endpoint `c91f2d7dd <https://github.com/fedora-infra/datagrepper/commit/c91f2d7dd63b75f0377f6e0fd0b46d07ce72c978>`_
- Implement /submit (without any database stuff yet) `1f4f4bef3 <https://github.com/fedora-infra/datagrepper/commit/1f4f4bef3dce802e88a2300c31cf60e0b04310a7>`_
- Change DataQuery obj implementation to make sense `d19aa5bd5 <https://github.com/fedora-infra/datagrepper/commit/d19aa5bd5aa397f65275799e656639c54968c81d>`_
- Remove everything that we won't be needing `620e93ec8 <https://github.com/fedora-infra/datagrepper/commit/620e93ec82fe44f332bee31ef2a10c2662b37ffd>`_
- Finish up /submit implementation. This should work `797c2a1ce <https://github.com/fedora-infra/datagrepper/commit/797c2a1cefbddbdba671441f11bc0acf84455d8d>`_
- Finish /submit endpoint `a6a9e76b5 <https://github.com/fedora-infra/datagrepper/commit/a6a9e76b5ad8f23ad9aaed2b294a534dd420c1a1>`_
- Add documentation for /submit (and /status) `c0c84d9ef <https://github.com/fedora-infra/datagrepper/commit/c0c84d9ef932ea3a4c6eebde4ac19617ffd1f3fa>`_
- Add /status endpoint `316a6767d <https://github.com/fedora-infra/datagrepper/commit/316a6767d0e4893cef9f9ed5af985d84a4d7097d>`_
- parse_from_* -> from_* `46f9c9c97 <https://github.com/fedora-infra/datagrepper/commit/46f9c9c9703fdd65f98e3179eb37ec309bfe3cdb>`_
- datetime.fromtimestamp requires a float() `2f8c98b1d <https://github.com/fedora-infra/datagrepper/commit/2f8c98b1dd642b22eecc4d7f02b2716206e58258>`_
- Merge pull request #50 from fedora-infra/feature/fix_end_timestamp `8483a75b6 <https://github.com/fedora-infra/datagrepper/commit/8483a75b687be7fd10c0a5822e542b3ef94a8af2>`_
- Merge branch 'develop' of github.com:fedora-infra/datagrepper into feature/submit-endpoint `c7aa92ccd <https://github.com/fedora-infra/datagrepper/commit/c7aa92ccdb3ee0bedc8c1c1158078d1919f03519>`_
- fedmsg so far `59016eb86 <https://github.com/fedora-infra/datagrepper/commit/59016eb86612b69a817f86f05e6b325b1d4c21dd>`_
- remove hello world message `7ed2ef447 <https://github.com/fedora-infra/datagrepper/commit/7ed2ef44766d488f317c7b057bf73094a486c81e>`_
- Fix status URL in docs `ef704a7a4 <https://github.com/fedora-infra/datagrepper/commit/ef704a7a4dce71e49c12fd90056eea88f68ef173>`_
- yeah fuck this advanced query language `90cac5a36 <https://github.com/fedora-infra/datagrepper/commit/90cac5a36a21e53df56370b627ffd11c3e6c2ed6>`_
- Implement running data queries `06bae01a9 <https://github.com/fedora-infra/datagrepper/commit/06bae01a9f7cba33849b8283a9e12e23455cf1a0>`_
- Add build to .gitignore `a6b212147 <https://github.com/fedora-infra/datagrepper/commit/a6b2121471bba03382cdca7bb3f9c739e11aba1f>`_
- Implement job runner as a part of fedmsg-hub `4493eef45 <https://github.com/fedora-infra/datagrepper/commit/4493eef45ceed7a6238b4239c48336c5b08182d8>`_
- Using 'job_id' and 'id' for the same thing is dumb `095e637e2 <https://github.com/fedora-infra/datagrepper/commit/095e637e25d923748756a2f1df0d43480ca114a8>`_
- Update docs `0ca7e1457 <https://github.com/fedora-infra/datagrepper/commit/0ca7e1457e43042a1118a42cc5f63a49820c5776>`_
- s/from_request/from_request_args/ `b9ccca2dc <https://github.com/fedora-infra/datagrepper/commit/b9ccca2dc7d11aa60596738f5eb01552fed32771>`_
- Merge pull request #51 from fedora-infra/feature/submit-endpoint `e8ef69d69 <https://github.com/fedora-infra/datagrepper/commit/e8ef69d6910dd30f3f4b88c82506630038ede081>`_
- Add /topics endpoint `37ff18cb4 <https://github.com/fedora-infra/datagrepper/commit/37ff18cb4f30715a8ebd27cb40eb7cfef10aad61>`_
- Remove dangling symlink `bce41824f <https://github.com/fedora-infra/datagrepper/commit/bce41824fbe96f82b522a1dc78661f524899ad46>`_
- Cache /topics endpoint `ba70a3132 <https://github.com/fedora-infra/datagrepper/commit/ba70a3132f127b9bc4a4534545b93d963931e9cf>`_
- Add docs for /topics `13c1abb40 <https://github.com/fedora-infra/datagrepper/commit/13c1abb409c7c6d44721c5b6cd87bb1266ca504d>`_
- Update README.rst `d4996b2f9 <https://github.com/fedora-infra/datagrepper/commit/d4996b2f94791fb378b8a8eafa8dc0010023aabb>`_
- Hey we have a prod instance now `5e3c06a0c <https://github.com/fedora-infra/datagrepper/commit/5e3c06a0c60fd4073e87a74b4655d3144af69b60>`_
- Remove unnecessary import `c4eccb1a5 <https://github.com/fedora-infra/datagrepper/commit/c4eccb1a52a03b9d2a36fda4861aac8cc8bdae5a>`_
- fix /topics in reference doc `f3f2c1902 <https://github.com/fedora-infra/datagrepper/commit/f3f2c1902ea1aaf251ad13096d3c0ea3fbce4c2e>`_
- Merge pull request #61 from fedora-infra/feature/topics-endpoint `a4b352b47 <https://github.com/fedora-infra/datagrepper/commit/a4b352b47dfc7ba138a0dbf6d2aee153dc0f3c74>`_
- Job runner deletes completed jobs after a set time `89705cdd0 <https://github.com/fedora-infra/datagrepper/commit/89705cdd00320433071705815d537259c5c633c3>`_
- Don't delete output immediately after `6a0015e4d <https://github.com/fedora-infra/datagrepper/commit/6a0015e4dcfa517b19db4b9c0eb88f710c71076f>`_
- Merge pull request #63 from fedora-infra/feature/job-runner-deletion `48c2267cd <https://github.com/fedora-infra/datagrepper/commit/48c2267cd1b33ec77661d87c6b3a96ffd37dc339>`_
- This should work, but doesn't `b89cf7d9a <https://github.com/fedora-infra/datagrepper/commit/b89cf7d9a491ff20529127f505889bcaa4c94b8e>`_
- Fix logging in `22126e9d7 <https://github.com/fedora-infra/datagrepper/commit/22126e9d7eef18ce0139fe81945af0a0c0eee028>`_
- Finish implementing auth `7a28a277f <https://github.com/fedora-infra/datagrepper/commit/7a28a277f64d1f89c777858c4f3498774fd64cf8>`_
- Fix error reporting `adb5865dc <https://github.com/fedora-infra/datagrepper/commit/adb5865dcbb930f211068288af138a038a5700b0>`_
- Make OpenID endpoint configurable `4e9afbc99 <https://github.com/fedora-infra/datagrepper/commit/4e9afbc99a95141df9899c070251c819d42a74eb>`_
- Remove a debugging line `32bb54a46 <https://github.com/fedora-infra/datagrepper/commit/32bb54a46857528f8679f2b258d301f54ba624e3>`_
- Merge pull request #64 from fedora-infra/feature/submit-auth `7f4c20541 <https://github.com/fedora-infra/datagrepper/commit/7f4c20541aba02ffa4bd16d03bc0967209b249e1>`_
- requirements.txt cleanup `e2d640360 <https://github.com/fedora-infra/datagrepper/commit/e2d640360f4f542562ef38a67427ae8ded4a6834>`_
- Update requirements.txt (closes #62) `d2b01bb9c <https://github.com/fedora-infra/datagrepper/commit/d2b01bb9c74a1710efeda475a9af223ed0dea252>`_
- 0.2.0 `d45d9c353 <https://github.com/fedora-infra/datagrepper/commit/d45d9c35398e2b672da34d8c4001315042244c00>`_
- Merge branch 'master' into develop `e163cc5b9 <https://github.com/fedora-infra/datagrepper/commit/e163cc5b90d95b1d1e23a859cf74e2da1e6c3775>`_
- Call __json__ on the Message instance, not the class. `d46145fe1 <https://github.com/fedora-infra/datagrepper/commit/d46145fe158232f62aeaef8b01cb7ed32c34947e>`_
- Merge pull request #67 from fedora-infra/feature/msg-jsonification-tweak `71ba52efc <https://github.com/fedora-infra/datagrepper/commit/71ba52efc68587aac14adbd8cf4ba24ec8971a10>`_
- Make assemble_timerange work if you aren't in EDT `12b6e4230 <https://github.com/fedora-infra/datagrepper/commit/12b6e4230486cd5bb72424c0e0ea29aead8f4a1d>`_
- Merge pull request #68 from fedora-infra/feature/timerange-test-tzfix `a64022f8c <https://github.com/fedora-infra/datagrepper/commit/a64022f8cde219f2a9c0408fb2f5bb6f793759fe>`_
- Add /id endpoint `1b0c11aa6 <https://github.com/fedora-infra/datagrepper/commit/1b0c11aa61b7d7437b5963dec44c0a035fb59821>`_
- Fix lockfile import for el6 version of lockfile `39ab240f7 <https://github.com/fedora-infra/datagrepper/commit/39ab240f77ad90f678c29fa9d41d06e18f91ff02>`_
- Merge pull request #69 from fedora-infra/feature/el6-lockfile `64ce23ec0 <https://github.com/fedora-infra/datagrepper/commit/64ce23ec00c3d875c4a403c72207498af6d00634>`_
- Make tarfile use compatible with Python 2.6 `5cbd285c1 <https://github.com/fedora-infra/datagrepper/commit/5cbd285c1fa7e92d959cb8739c00e99fea5f26ef>`_
- Add .travis.yml `3e14b16a1 <https://github.com/fedora-infra/datagrepper/commit/3e14b16a17a2584a36b2fd8ac9ac0df7f7632df0>`_
- If tarfile runs into a problem, close it; if lzma runs into a problem, close it and delete the file `9736a22b7 <https://github.com/fedora-infra/datagrepper/commit/9736a22b7a881611fe8d9cac9285ebf8c80d3de9>`_
- PEP 8 `4436ccf53 <https://github.com/fedora-infra/datagrepper/commit/4436ccf53ddde28b886b4b451f2bee6fe0681e98>`_
- Merge branch 'develop' of github.com:fedora-infra/datagrepper into feature/py26-tarfile `dfbfe0693 <https://github.com/fedora-infra/datagrepper/commit/dfbfe06931791dfd7cafdb26cf9122045ad3caa0>`_
- travis: install liblzma-dev before python setup.py install `86024dfce <https://github.com/fedora-infra/datagrepper/commit/86024dfce46f3131621725cfabb986c697c05033>`_
- Merge branch 'develop' of github.com:fedora-infra/datagrepper into feature/py26-tarfile `1eb281865 <https://github.com/fedora-infra/datagrepper/commit/1eb281865d2f78c9f56e28010cd0eaaf7a1e6b46>`_
- Merge pull request #73 from fedora-infra/feature/py26-tarfile `9a6ba11ef <https://github.com/fedora-infra/datagrepper/commit/9a6ba11efbbd31ade73439be4cd82add51f5da98>`_
- Merge branch 'develop' into feature/uuid-support `030999ecd <https://github.com/fedora-infra/datagrepper/commit/030999ecd84c895021cb0c5a0872f7cebf84c7b3>`_
- Fix /id endpoint `5870a4e5f <https://github.com/fedora-infra/datagrepper/commit/5870a4e5fb79c79e2c814389e7328cb4dfd164cc>`_
- Fix consumer not running on non-dev environments `6319ce9a6 <https://github.com/fedora-infra/datagrepper/commit/6319ce9a6ee26a1b4cef780bb80b64f6340085b5>`_
- Set job status to 'failed' if a traceback occurs `2484efd98 <https://github.com/fedora-infra/datagrepper/commit/2484efd98fda8855a02d6a7c335a72174bbe8c11>`_
- Merge pull request #75 from fedora-infra/feature/runner-fixes `e47aeff24 <https://github.com/fedora-infra/datagrepper/commit/e47aeff248774240257e61ff6b116dd8747e0d83>`_
- Not including 'id' on /id is a 400 `5809216b7 <https://github.com/fedora-infra/datagrepper/commit/5809216b7b0ce756f3c7abca2ee66fa3c7d28b9f>`_
- Merge branch 'develop' into feature/uuid-support `de6a6b9e6 <https://github.com/fedora-infra/datagrepper/commit/de6a6b9e637937ab2ee1555edc9fb078f8d1e46c>`_
- Merge pull request #74 from fedora-infra/feature/uuid-support `2479d5000 <https://github.com/fedora-infra/datagrepper/commit/2479d50000c9a67105231cc6f5172230c122fe79>`_

0.1.4
=====

- Minor pep8 fix. `c5fcc4484 <https://github.com/fedora-infra/datagrepper/commit/c5fcc4484ab41c701cbae246a48e0cc83245896a>`_
- Typofix. `ccbdd1684 <https://github.com/fedora-infra/datagrepper/commit/ccbdd1684b9ec58921733c75394c093a2a62527b>`_
- Another typofix. `4212690c3 <https://github.com/fedora-infra/datagrepper/commit/4212690c39fa3b2e8a8110f56b7bfd1c86dee67f>`_
- Remove the spec file. `f45ff6614 <https://github.com/fedora-infra/datagrepper/commit/f45ff66149fae564f76af0adcc3bb356cbc0f50d>`_
- Merge pull request #35 from fedora-infra/feature/no-spec `f501a43d6 <https://github.com/fedora-infra/datagrepper/commit/f501a43d6d52a62058532c52e9f788e4fba6caad>`_
- Merge branch 'master' into develop `dd0e318d5 <https://github.com/fedora-infra/datagrepper/commit/dd0e318d567a891597eb5a89ad740b83b4318a0f>`_
- Typofix. `6f5a58f2a <https://github.com/fedora-infra/datagrepper/commit/6f5a58f2a04dee17b882f47c263850b6736c9496>`_
- Allow user to specify order of results. `bc73d1b48 <https://github.com/fedora-infra/datagrepper/commit/bc73d1b48c3af5a0def3f4e9ecbec2d55002bb9f>`_
- Constrain version of datanommer.models. `d71979e7b <https://github.com/fedora-infra/datagrepper/commit/d71979e7b877b9235c7797f9d6665c22d38e9d6a>`_
- Use a dev url in the dev config. `e5fa67213 <https://github.com/fedora-infra/datagrepper/commit/e5fa6721383efdeb37d63082330254fba7233695>`_
- Mention the order argument in the index docs. `e4fcc7e8b <https://github.com/fedora-infra/datagrepper/commit/e4fcc7e8ba77b647c347e56b3cdc3c9abdce9df3>`_
- Merge pull request #39 from fedora-infra/feature/ordering-results `c703d8261 <https://github.com/fedora-infra/datagrepper/commit/c703d82610c1677081b1804b26bf2e443245e1be>`_
- Use abadger's suggested scheme. `2fea62f28 <https://github.com/fedora-infra/datagrepper/commit/2fea62f2809fa02f038ac50bea23328ea1823f1d>`_
- Tell pep8.me and the pep8 tool to reduce their zeal. `eb685666c <https://github.com/fedora-infra/datagrepper/commit/eb685666c2c46d4b679fa7e0633f6a9271bf455b>`_
- Merge pull request #32 from fedora-infra/feature/pep8 `412e76f9a <https://github.com/fedora-infra/datagrepper/commit/412e76f9a0ebdd5b47ee9d7241d32fdf1939b677>`_
- Allow the user to retrieve the last ``rows_per_page`` items regardless of the time `c8c0ca8d0 <https://github.com/fedora-infra/datagrepper/commit/c8c0ca8d093bb97734d78503e03e6868ff304994>`_
- Reorganize the app to make the datetime stuff testable. `171fbf57e <https://github.com/fedora-infra/datagrepper/commit/171fbf57e7821587a626d9ffbd93f236c3807087>`_
- Some tests for the datetime stuff. `fafc062a6 <https://github.com/fedora-infra/datagrepper/commit/fafc062a61c9dc8be45e9142a3d5e2da6557b830>`_
- Change the docs for one of the datetime combinations. `625dc2b39 <https://github.com/fedora-infra/datagrepper/commit/625dc2b39cdc9e69cb23eb8564c1c6e8f0f47f42>`_
- Fix up our logic to get all tests passing. `517a5e84f <https://github.com/fedora-infra/datagrepper/commit/517a5e84f16f99d0439da8bc3666301746f571d6>`_
- PEP8 `7fd9cf8d8 <https://github.com/fedora-infra/datagrepper/commit/7fd9cf8d84cc8b82f606a27209044959c31ec77c>`_
- A technicality. `ad2d979eb <https://github.com/fedora-infra/datagrepper/commit/ad2d979ebbf8d9797cb15f183a5f27b70bf6eab4>`_
- Merge pull request #43 from fedora-infra/feature/docs-jsonp `02bff8289 <https://github.com/fedora-infra/datagrepper/commit/02bff8289fc37dd7336ac962ad03f04411a30c2a>`_
- Merge pull request #42 from fedora-infra/retrieve_last_items `fa95e688b <https://github.com/fedora-infra/datagrepper/commit/fa95e688bab18473e3105ad00985e58f43331b78>`_
- Add option to return metadata with the raw message `cc0775d95 <https://github.com/fedora-infra/datagrepper/commit/cc0775d95a1ada9ccf4bdc9bdff9e5da8632b849>`_
- Sets take a list. `51b327abc <https://github.com/fedora-infra/datagrepper/commit/51b327abc23313b91013d31a5857acf0480805e8>`_
- Indentation. `e101736ba <https://github.com/fedora-infra/datagrepper/commit/e101736ba228f8bcd555e41cbf62ed7c110b752b>`_
- Return the argued meta attributes back to the user. `eb69e55b2 <https://github.com/fedora-infra/datagrepper/commit/eb69e55b2f08c9e2f74f1a9f69ccee9933c17205>`_
- Fix checking that the meta provided are part of the allowed set `bd31da59c <https://github.com/fedora-infra/datagrepper/commit/bd31da59c0fd76d105a90badbacfde273c1f7dc2>`_
- Usernames should be plural here. `22403b817 <https://github.com/fedora-infra/datagrepper/commit/22403b8173e93a96b397e71f475531ea32f1648a>`_
- Initialize fedmsg metadata processors at startup. `70af7bfa6 <https://github.com/fedora-infra/datagrepper/commit/70af7bfa62960713cf320ae25ab32220fecd5e1f>`_
- fedmsg.meta is expecting a dict. `8890002f7 <https://github.com/fedora-infra/datagrepper/commit/8890002f7280c89b6418447f1480707d6f11c0ab>`_
- Let flask handle listification for us. `91227188e <https://github.com/fedora-infra/datagrepper/commit/91227188e5b6dfbf528f0b13d5caac39e33bddaa>`_
- Convert messages from sqlalchemy objects to json-like dicts earlier in the pipeline so we can manipulate them. `40bcf08f6 <https://github.com/fedora-infra/datagrepper/commit/40bcf08f6d185c668a6c8fd8cc3807abdce4c2c5>`_
- Pluralization. `45dd762f6 <https://github.com/fedora-infra/datagrepper/commit/45dd762f6af42da1f16874795131b5b266bdc13c>`_
- Fix up the runserver script. `96a5fb72a <https://github.com/fedora-infra/datagrepper/commit/96a5fb72acf2c15722f88b8269d5acc3c8762903>`_
- Convert set to list before trying to serialize. `4e1df5b29 <https://github.com/fedora-infra/datagrepper/commit/4e1df5b29c9c80431a4cf8a2d33388436861e3a3>`_
- Re-introduce the use of util.assemble_timerange.  It got lost in a rebase. `2c651f25a <https://github.com/fedora-infra/datagrepper/commit/2c651f25ab46523649c8a2844e85951f139f8628>`_
- Merge pull request #41 from fedora-infra/meta_endpoint `ef7a72a88 <https://github.com/fedora-infra/datagrepper/commit/ef7a72a888e4080d4fb6769f647ba6aaa2f64d27>`_

0.1.3
=====

- Include docs/ dir in tarball. `b364debf6 <https://github.com/fedora-infra/datagrepper/commit/b364debf61d5f5f613007ec105689c529c9f8838>`_
- Merge pull request #28 from fedora-infra/feature/include-docs-in-tarball `63e44f64f <https://github.com/fedora-infra/datagrepper/commit/63e44f64fb0aee866d0c4f5d4189ef77f3e74f53>`_
- Second try at using a configurable URL for the docs.  Sorry for the merge mess before. `397c3a141 <https://github.com/fedora-infra/datagrepper/commit/397c3a141b8016aed34d4b2d6ba5305dfdf605fa>`_
- Downgrade .rst content if docutils is too old to handle it.  Fixes #29. `b1e34f87e <https://github.com/fedora-infra/datagrepper/commit/b1e34f87e8be102e6095045f0f0de373f69bf522>`_
- Be more careful when comparing docutils versions. `3ddf5668e <https://github.com/fedora-infra/datagrepper/commit/3ddf5668e6f67e10c4c0340f5883185c35bed1c8>`_
- Allow for ajax/jsonp results from the /raw url. `c94c9eb2c <https://github.com/fedora-infra/datagrepper/commit/c94c9eb2c7b0570da4812d0b6c4f88363b7394a9>`_
- Simplify that conditional. `a0ba7f778 <https://github.com/fedora-infra/datagrepper/commit/a0ba7f7785daf356067df310ca7532348395fc15>`_
- Merge pull request #33 from fedora-infra/feature/codeblock-downgrade `78c42d6da <https://github.com/fedora-infra/datagrepper/commit/78c42d6da84ff1690d1d3bc59201951230bcaff4>`_
- Merge pull request #34 from fedora-infra/feature/jsonp `5f5e0a151 <https://github.com/fedora-infra/datagrepper/commit/5f5e0a15111cd6cab8ff1c5219e75f5aa8fa0480>`_
- Merge branch 'feature/configurable-url-take-two' into develop `91eb38d5c <https://github.com/fedora-infra/datagrepper/commit/91eb38d5c7d2ca600c220d14d2a53a44cf8a0147>`_

0.1.2
=====

- Merge branch 'master' into develop `67f604d67 <https://github.com/fedora-infra/datagrepper/commit/67f604d675382add2a86a7c0cff3b12bcb553d78>`_
- Remove old-templates `dea003299 <https://github.com/fedora-infra/datagrepper/commit/dea003299e3ca677c21141e026938cb7cdc5f860>`_
- Be able to load docs from multiple rst files `a997365bf <https://github.com/fedora-infra/datagrepper/commit/a997365bfc88c3e81dcb7c0492c0858f4b29bc90>`_
- Comment out remotely-hosted touch icons `edbfa74c1 <https://github.com/fedora-infra/datagrepper/commit/edbfa74c14ba01412a2ef15b3eddc4457b39c483>`_
- Merge branch 'develop' into feature/reference `27678502d <https://github.com/fedora-infra/datagrepper/commit/27678502d236f7284a6b25c50492d986eb0a4c0b>`_
- Get most of the /raw reference done `70c47cb26 <https://github.com/fedora-infra/datagrepper/commit/70c47cb26a917b4d550076b05d59904c569d7ff0>`_
- Finish up docs for /raw `2a8905f24 <https://github.com/fedora-infra/datagrepper/commit/2a8905f242a71a067c137df07b14082bb7934f6a>`_
- Documentation style adjustments `fdd266bb6 <https://github.com/fedora-infra/datagrepper/commit/fdd266bb6f1561a7577330baf12c88f5737d7c88>`_
- Add reference page to navbar `b88ae0f65 <https://github.com/fedora-infra/datagrepper/commit/b88ae0f6562cc3739d418e4030334c2bae66efd7>`_
- Don't need show_jumbotron anymore `4ff46275d <https://github.com/fedora-infra/datagrepper/commit/4ff46275d0965fecff78dc3cacb9dc14a8a33c33>`_
- Use user's URL in command-line examples `79bae0e7e <https://github.com/fedora-infra/datagrepper/commit/79bae0e7e392696bd44a068b532d0ac813c860d4>`_
- Make docs the full width of the content `392310ace <https://github.com/fedora-infra/datagrepper/commit/392310aceecc427ed49687929e7d6b4eb7c8e7e6>`_
- Whitespace fix `ffa6e4a13 <https://github.com/fedora-infra/datagrepper/commit/ffa6e4a13953ad422f582a5f2506fcaa91fc9da8>`_
- Fix ellipsis `32ecd182a <https://github.com/fedora-infra/datagrepper/commit/32ecd182a8de2fbf9fad1159755ba72ab8827bfb>`_
- Minor changes to index docs `b2d2973fb <https://github.com/fedora-infra/datagrepper/commit/b2d2973fb5b852931e79f12c70ca133946fbf1c6>`_
- Small changes to reference docs `cb1f896b7 <https://github.com/fedora-infra/datagrepper/commit/cb1f896b7af66dbd7e8744d7d8bc7593540deb28>`_
- Merge pull request #24 from fedora-infra/feature/reference `bce825348 <https://github.com/fedora-infra/datagrepper/commit/bce82534897188b33c9597c03f90503c4cb73721>`_
- Add COPYING file (GPL version 2) `fba281cc2 <https://github.com/fedora-infra/datagrepper/commit/fba281cc2eeec98fa381086ca9b9d513a5a5859e>`_
- Add license boilerplate in at least one file `97f391376 <https://github.com/fedora-infra/datagrepper/commit/97f391376432f8e99b58413e601f9f355ff32fcc>`_
- Merge branch 'master' into develop `0a0f9764f <https://github.com/fedora-infra/datagrepper/commit/0a0f9764fc0027382ed7958f386e1a862113f726>`_
- Update RPM spec to current revision (RHBZ 955781) `1eb5c81d0 <https://github.com/fedora-infra/datagrepper/commit/1eb5c81d0bc6cfe72caffad240c203ad5f8db8ff>`_
- Update spec `071f11a4e <https://github.com/fedora-infra/datagrepper/commit/071f11a4e1045e472b437193c12cf8adbee9d29b>`_
- Support timedelta_to_seconds on py2.6. `9847b7cda <https://github.com/fedora-infra/datagrepper/commit/9847b7cdaa5b6fb069819d20c15d3ec2674b6af7>`_
- Pass the delta to timedelta_to_seconds `e71ce03c7 <https://github.com/fedora-infra/datagrepper/commit/e71ce03c78b6196d18cc8963b591b4d4d97bca2d>`_
- Use a configurable URL for the API docs. `d8a3ed0d1 <https://github.com/fedora-infra/datagrepper/commit/d8a3ed0d1ceb709aa18bcc5fdf4f862593c3bfc6>`_
- Make the quotes consistent. `22d0d518e <https://github.com/fedora-infra/datagrepper/commit/22d0d518ee804cf90d65e35af5ea5f7a02803c9d>`_
- Merge branch 'feature/update-docs' into develop `61656a4ff <https://github.com/fedora-infra/datagrepper/commit/61656a4ff90578e8e12d9144fef85a53eca1feb5>`_
- Merge pull request #26 from fedora-infra/feature/timedelta-to-seconds `b193a47a7 <https://github.com/fedora-infra/datagrepper/commit/b193a47a7208773ae18926905b64baee2777ceb6>`_

0.1.1
=====

- Add COPYING file (GPL version 2) `b666a5877 <https://github.com/fedora-infra/datagrepper/commit/b666a5877fa07e04c0cc6daa011a108dc6d4d21d>`_
- Add license boilerplate in at least one file `269afe2c2 <https://github.com/fedora-infra/datagrepper/commit/269afe2c2f33daa07e1c0ce9cb2b2338b362a462>`_
- Bump version to 0.1.1 `d8119fefa <https://github.com/fedora-infra/datagrepper/commit/d8119fefa01154c115d34fdd986a4164867627bb>`_
