%#template to generate a HTML form from a list
<style>
input[type=submit] {
    width: 10em;
    border: 3px solid blue;
    margin: 50px;
    color: red;
    font-size: 40px;
}
</style>

<h1>Brought to you by your local IT Team</h1>

<p>Hello {{userName}}:</p>

<p>Please confirm that you want you PaperCut MF balance (${{userCredit}}) credited back to your student account</p>

<form action="/refund/{{user}}" method=get>

    <input type="hidden" name="amount" value="{{userCredit}}">

    <input type="submit" name="refund" value="Refund ${{userCredit}}">
    <input type="submit" name="cancel" value="cancel">

</form>

<p><em>NOTE</em>: After the refund you will be unable to print or use the campus copiers until you credit more funds to your PaperCut MF account</p>
