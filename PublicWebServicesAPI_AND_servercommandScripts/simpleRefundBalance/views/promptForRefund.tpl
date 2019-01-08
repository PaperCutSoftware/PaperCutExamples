%#template to generate a HTML form from a list

<p>Hello {{user}}: Please confirm that you want you PaperCut balance (${{userCredit}}) credited back to your student account?</p>

<form action="/refund/{{user}}" method=get>


    <input type="hidden" name="amount" value="{{userCredit}}">

    <input type="submit" name="refund" value="Refund ${{userCredit}}">
    <input type="submit" name="cancel" value="cancel">
</form>

