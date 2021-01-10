import pytest
from argparse import ArgumentParser
from stackoverflow_analytics import StackOverflowAnalyzer, setup_parser, setup_logging

DATASET_SAMPLE = """<row Id="203358" PostTypeId="1" CreationDate="2008-10-15T00:44:56.847" Score="5" ViewCount="2239" Body="&lt;p&gt;I want to set a style on the first and last TabItems in a TabControl, and have them updated as the visibility of the TabItems is changed.  I can't see a way to do so with triggers.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;What we're after looks like this:&lt;/p&gt;&#xA;&#xA;&lt;pre&gt;| &gt; &gt; &gt; |&lt;/pre&gt;&#xA;&#xA;&lt;p&gt;And the visibility of TabItems are determined by binding.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;I do have it working in code.  On TabItem visibility changed, enumerate through TabItems until you find the first visible one.  Set the style on that one.  For all other visible TabItems, set them to the pointy style (so that the previously first visible one is now pointy).  Then start from the end until you find a visible TabItem and set the last style on that one.  (This also lets us address an issue with TabControl where it will display the content of a non-visible TabItem if none of the visible TabItems are selected.)&lt;/p&gt;&#xA;&#xA;&lt;p&gt;There's undoubtably improvements I could make to my method, but I'm not convinced that it IS the right approach.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;How would you approach this?&lt;/p&gt;&#xA;" OwnerUserId="28074" LastEditorUserId="66708" LastEditorDisplayName="Jexia" LastEditDate="2010-10-15T00:37:22.290" LastActivityDate="2013-02-06T17:45:43.123" Title="Setting style on first and last visible TabItem of TabControl" Tags="&lt;.net&gt;&lt;wpf&gt;&lt;xaml&gt;&lt;tabcontrol&gt;&lt;tabitem&gt;" AnswerCount="3" CommentCount="2" FavoriteCount="1" />
<row Id="204202" PostTypeId="1" AcceptedAnswerId="204211" CreationDate="2008-10-15T09:55:58.573" Score="12" ViewCount="25302" Body="&lt;p&gt;I would like to know exactly how the &quot;Is&quot; command works in Linux and Unix.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;As far as I know, ls forks &amp;amp; exec to the linux/unix shell and then gets the output (of the current file tree. eg./home/ankit/).  I need a more detailed explanation, as I am not sure about what happens after calling fork.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;Could any one please explain the functionality of the 'ls' command in detail?&lt;/p&gt;&#xA;" OwnerUserId="24813" OwnerDisplayName="Ankit S" LastEditorUserId="672" LastEditorDisplayName="kogus" LastEditDate="2008-10-28T20:58:09.303" LastActivityDate="2013-05-14T02:23:29.077" Title="How does the 'ls' command work in Linux/Unix?" Tags="&lt;linux&gt;&lt;unix&gt;&lt;open-source&gt;&lt;operating-system&gt;&lt;solaris&gt;" AnswerCount="5" CommentCount="0" FavoriteCount="9" />	
<row Id="207239" PostTypeId="1" AcceptedAnswerId="207245" CreationDate="2008-10-16T02:35:24.050" Score="1" ViewCount="2944" Body="&lt;p&gt;My organization is considering using Jabber as an agnostic device to device to application messaging protocol.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;Does anyone know of the best practice existing Microsoft competitor to Jabber?  Or, an emerging competitor?  And, if so, a good URL reference to get a jump start?&lt;/p&gt;&#xA;&#xA;&lt;p&gt;Website for Jabber:&#xA;&lt;a href=&quot;http://www.jabber.org/web/Main_Page&quot; rel=&quot;nofollow noreferrer&quot;&gt;http://www.jabber.org/web/Main_Page&lt;/a&gt;&lt;/p&gt;&#xA;" OwnerUserId="24126" OwnerDisplayName="pearcewg" LastEditorUserId="24126" LastEditorDisplayName="pearcewg" LastEditDate="2008-10-16T03:08:13.780" LastActivityDate="2010-12-09T16:37:28.817" Title="Microsoft alternative to Jabber?" Tags="&lt;.net&gt;&lt;wcf&gt;&lt;messaging&gt;&lt;xmpp&gt;" AnswerCount="5" CommentCount="0" FavoriteCount="1" ClosedDate="2012-09-11T08:17:56.657" />	
<row Id="4142091" PostTypeId="1" AcceptedAnswerId="5708168" CreationDate="2010-11-10T07:23:37.527" Score="3" ViewCount="262" Body="&lt;p&gt;For example:&lt;/p&gt;&#xA;&#xA;&lt;p&gt;&lt;a href=&quot;http://jqueryui.com/demos/progressbar/#animated&quot; rel=&quot;nofollow&quot;&gt;http://jqueryui.com/demos/progressbar/#animated&lt;/a&gt;&lt;/p&gt;&#xA;&#xA;&lt;p&gt;The progress bar has it's progress increasing from 0 to 100 percent but it still has some animation to it.  This helps show the user something is still happening even if the bar is stopped at one point for a moment.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;When I set the progress bar to indeterminate, it no longer shows the progress.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;Is there a built in way to accomplish this or will I need to subclass ProgressBar?&lt;/p&gt;&#xA;" OwnerUserId="445348" LastActivityDate="2011-06-30T08:34:23.173" Title="Is there a way to have a Progress Bar both progress and have the indeterminate animation?" Tags="&lt;android&gt;&lt;progress-bar&gt;" AnswerCount="1" CommentCount="0" FavoriteCount="0" />	
<row Id="4147820" PostTypeId="1" AcceptedAnswerId="4147949" CreationDate="2010-11-10T18:36:56.130" Score="3" ViewCount="298" Body="&lt;p&gt;I have a query that looks like the following:&lt;/p&gt;&#xA;&#xA;&lt;pre&gt;&lt;code&gt;SELECT someString  FROM&#xA;(&#xA;    SELECT someString FROM someTable&#xA;    WHERE someField = 1&#xA;) X&#xA;WHERE dbo.fnMyClrScalarFunction(X.someString) = 0&#xA;&lt;/code&gt;&lt;/pre&gt;&#xA;&#xA;&lt;p&gt;The problem is that the query optimizer is moving the UDF inside the subquery, where it is applied before the fairly restrictive 'someField = 1' condition.  Unfortunately, the UDF is not exactly speedy, and this results in terrible performance.  Is there any way to prevent this (aside from using a temp table) or to establish to sql server that the UDF is expensive?&lt;/p&gt;&#xA;&#xA;&lt;p&gt;Thanks in advance&lt;/p&gt;&#xA;" OwnerUserId="199751" LastActivityDate="2010-12-15T15:18:15.430" Title="SQL Server - CLR stored proc in scalar function as filter not weighted properly in query optimizer ==&gt; BAD EXECUTION PLAN" Tags="&lt;sql&gt;&lt;sql-server&gt;&lt;sql-server-2008&gt;&lt;clrstoredprocedure&gt;&lt;sql-execution-plan&gt;" AnswerCount="2" CommentCount="3" />	
invalid row
<row Id="4147820" PostTypeId="1" CreationDate="2020-11-10T18:36:56.130" Score="500" Title="repeat repeat repeat repeat" AnswerCount="2" CommentCount="3" />	
"""
STOPWORDS_SAMPLE = """a
about
above
across
after
afterwards
again
against
all
almost
"""
QUERIES_SAMPLE = """2008,2008,5
2009,2011,10
2007,2007,4
2020,2020,2
invalid,query
"""


@pytest.fixture
def dataset_sample(tmpdir):
    dataset_fio = tmpdir.join('stackoverflow_sample.xml')
    dataset_fio.write(DATASET_SAMPLE)
    return dataset_fio


@pytest.fixture
def stopwords_sample(tmpdir):
    stopwords_fio = tmpdir.join('stopwords_sample.txt')
    stopwords_fio.write(STOPWORDS_SAMPLE)
    return stopwords_fio


@pytest.fixture
def queries_sample(tmpdir):
    queries_fio = tmpdir.join('queries_sample.csv')
    queries_fio.write(QUERIES_SAMPLE)
    return queries_fio


def test_analyzer_can_process_questions_stopwords_and_queries(dataset_sample, stopwords_sample, queries_sample):
    analyzer = StackOverflowAnalyzer(stopwords_sample, dataset_sample)
    query_answer = analyzer.query(queries_sample)
    assert len(query_answer) == 4
    assert '500' in query_answer[3]


def test_can_setup_parser_and_logging():
    setup_logging()
    parser = ArgumentParser(prog='stackoverflow_analytics')
    setup_parser(parser)
