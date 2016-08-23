%#template to generate a HTML form from a list

<p>Shared Accounts for {{user}}:</p>

<form action="/setdefaultsharedaccount/{{user}}" method=get>
    %for row in rows:
    <input type="radio" name="account" value="{{row}}">{{row}}</br>
    %end

    <input type="submit" name="save" value="save">
    <input type="submit" name="cancel" value="cancel">
</form>

