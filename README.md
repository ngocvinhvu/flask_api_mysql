# flask_api_mysql

Link: http://34.72.165.174/api/v0/customers

# Endpoint: 

## method = ['GET', 'POST', 'PUT', 'DELETE']
- /api/v0/customers/<customerNumber>
- /api/v0/employees/<employeeNumber>
- /api/v0/offices/<officeCode>
- /api/v0/orderdetails/<orderNumber>
- /api/v0/orders/<orderNumber>
- /api/v0/payments/<customerNumber>
- /api/v0/productlines/<productLine>
- /api/v0/products/<productCode>

## GET list of data
- /api/v0/customers # filter_by: country, contactFirstname # sort_by any field
- /api/v0/employees # filter_by: firstName, reportsTo # sort_by any field
- /api/v0/offices # filter_by: city, phone # sort_by any field
- /api/v0/orderdetails # filter_by: productCode, quantityOrdered # sort_by any field
- /api/v0/orders # filter_by: orderDate, requiredDate # sort_by any field
- /api/v0/payments # filter_by: paymentDate, checkNumber # sort_by any field
- /api/v0/productlines # filter_by: textDescription, htmlDescription # sort_by any field
- /api/v0/products # filter_by: productName, productLine # sort_by any field
