%#template to generate a HTML form from a list

<p>Hello {{user}}: please enter the amount you want to deposit into your PaperCut account</p>

<form action="/topUp/{{user}}" method=get>

    <input type="number" name="amount" value="00">

    <input type="submit" name="pay" value="pay">
    <input type="submit" name="cancel" value="cancel">
</form>

