select tbl_printer.server_name,  tbl_printer.printer_name, tbl_printer_attribute.attrib_name, tbl_printer_attribute.attrib_value
from tbl_printer_attribute, tbl_printer
where tbl_printer_attribute.printer_id = tbl_printer.printer_id
and tbl_printer_attribute.attrib_name like 'cost.%';

