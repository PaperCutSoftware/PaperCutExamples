%#template to generate a HTML form from a list

% if defined("error_text"):
    <em>{{error_text}}</em><br/><br/>
% end


<p>Hello {{user}}: please enter the amount you want to deposit into your PaperCut account</p>
<p>
Note: Minimum deposit is 0.05, maximum is 10.00 and only multiples of 0.05 may be entered

<form action="/topUp/" method="GET">

    <input type="number" name="amount" value="0.00" min="0.05" max="10.00" step="0.05">

    <input type="submit" name="pay" value="pay">
    <input type="submit" name="cancel" value="cancel">

    <input type="hidden" name="user" value="{{user}}">
    <input type="hidden" name="return_url" value="{{return_url}}">

</form>
