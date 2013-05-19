Research Flask/SQLAlchemy migration tool for when creating new DB elements.
Research Flask/SQLAlchemy migration tool for when creating new DB elements.
Check sanitation with http://xenomachina.com/testbed.xml

Planned API
===========
Below are some short details/notes/plans of how the API should
look like.

Feeds
=====
<table>
    <tr>
        <th>Resource</th>
        <th>POST</th>
        <th>GET</th>
        <th>PUT</th>
        <th>DELETE</th>
        <th>Status</th>
    </tr>

    <tr>
        <td>/feeds</td>
        <td>Create a new feed.</td>
        <td>Get all feeds for the logged in user.</td>
        <td>Bulk update feeds.</td>
        <td>Delete all feeds for the user.</td>
        <td>No work started.</td>
    </tr>

    <tr>
        <td>/feeds/{feed id}</td>
        <td>Error.</td>
        <td>Get the feed data for the specific feed.</td>
        <td>Update the feed</td>
        <td>Delete the feed.</td>
        <td>No work started.</td>
    </tr>
</table>

/feeds details
==============
* Sending a POST request should create a new feed, the request should be
JSON in the expected format.

* Sending a GET request should return a list of all the feeds,
maybe there should be a limit and offset for this?

* PUT request should do a bulk update of feeds, and the request
should include a list of feeds to update.

* DELETE request should delete all the feeds for that user.

/feeds/{feed id} details
===================
* Sending a POST request here should return a error, since this is
not the correct way to create a feed, the id should be created by
the server and not the client.

* Sending a GET request should return the details of the feed with
the requested ID. Maybe it should return entries as well?

* PUT updates the feed.

* DELETE deletes the feed.


Entries
=======
<table>
    <tr>
        <th>Resource</th>
        <th>POST</th>
        <th>GET</th>
        <th>PUT</th>
        <th>DELETE</th>
        <th>Status</th>
    </tr>

    <tr>
        <td>/entries</td>
        <td>Error.</td>
        <td>Get all entries for the logged in user.</td>
        <td>Bulk update entries.</td>
        <td>Error.</td>
        <td>No work started.</td>
    </tr>

    <tr>
        <td>/entries/{feed id}</td>
        <td>Error.</td>
        <td>Get all the entries for that feed.</td>
        <td>Bulk update the entries for that feed.</td>
        <td>Error.</td>
        <td>No work started.</td>
    </tr>

    <tr>
        <td>/entries/{feed id}/{entry id}</td>
        <td>Error.</td>
        <td>Get that entry's data.</td>
        <td>Mark that entry read.</td>
        <td>Error.</td>
        <td>No work started.</td>
    </tr>
</table>

/entries details
================
* Clients cannot create entries so POST should return a error.

* A GET request should return all the entries for the logged in
user in. There should be a limit and offset, returning all entries
is too much data.

* A PUT request should bulk update a list of entries, the only
update that can be done for entries is marking them as read.

* Cannot delete a feed so DELETE should return a error.

/entries/{feed id}
==================
* Clients cannot add a entry to a feed, so this should return a
error.

* A GET request should return all entries for that feed, this
request will have a limit and offset.

* A PUT request should bulk update entries for this feed and mark
them read.

* Cannot delete a entry so DELETE request should return a error.


/entries/{feed id}/{entry id}
=============================
* Cannot create a feed so POST should return a error.

* A GET should return that entry's data.

* A PUT should mark that entry as read.

* Cannot delete a entry so DELETE request should return a error.

Categories
=======
<table>
    <tr>
        <th>Resource</th>
        <th>POST</th>
        <th>GET</th>
        <th>PUT</th>
        <th>DELETE</th>
        <th>Status</th>
    </tr>

    <tr>
        <td>/category</td>
        <td>Create a new category.</td>
        <td>Get all categories for the logged in user.</td>
        <td>Bulk update categories.</td>
        <td>Delete all categories.</td>
        <td>No work started.</td>
    </tr>

    <tr>
        <td>/category/{category id}</td>
        <td>Error.</td>
        <td>Get all the data for that category.</td>
        <td>Update that category.</td>
        <td>Delete that category.</td>
        <td>No work started.</td>
    </tr>
</table>

/category details
=================
* POST should create a new category.

* GET should return all the categories for the logged in user.

* PUT does a bulk update of the categories.

* DELETE will delete all the categories for the user.

/category/{category id}
=======================
* Cannot create a category with a specific ID, so this should
return a error.

* Get all the data for that entry, this will be a list of feeds.

* PUT will update that specific feed.

* DELETE will delete that feed. Should the feeds be removed as well?
