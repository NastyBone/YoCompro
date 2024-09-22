### TODO

- Endpoints X
- Relations
- Login X
- Classes X
- Auth X
- Decorators

# MODULES

#### USERS X

- CREATE
- EDIT
- FIND ONE
- FIND MANY
- DELETE

#### AUTH

- REGISTER
- LOG IN
- LOG OUT
- FORGOT PASSWORD

#### BUSSINESS

- CREATE X
- UPDATE X
- FIND MANY X
- FIND ONE X
- DELETE X
- FIND BY NEAREST -- ?
- FIND BY SEARCH X
- FIND BY POPULAR X
- FIND BY TAG
- FIND BY OWNER X
- FIND BY OWNER AND POPULAR
- VERIFY x

#### STOCK X

- CREATE
- UPDATE
- FIND MANY
- FIND ONE
- DELETE
- FIND BY PRODUCT
- FIND BY BUSSINESS

#### PRODUCTS

- CREATE
- UPDATE
- FIND MANY
- FIND ONE
- DELETE
- FIND BY SEARCH
- FIND BY TAGS
- FIND BY POPULAR
- FIND BY NEAREST -- ?
- FIND BY BRAND
- FIND BY DISCOUNTS
- FIND BY ALL DISCOUNTS
- VERIFY

#### BRANDS X

- CREATE
- UPDATE
- FIND MANY
- FIND ONE
- DELETE
- FIND BY SEARCH
- FIND BY POPULAR
- VERIFY

#### RATINGS X

- CREATE
- UPDATE
- FIND
- DELETE
- FIND BY USER
- FIND BY PRODUCT
- FIND BY BUSSINESS

#### LISTS X

- CREATE
- UPDATE
- FIND
- DELETE
- FIND BY USER

#### TAGS X

- CREATE
- UPDATE
- FIND MANY
- FIND ONE
- DELETE
- VERIFY

# EXTRAS

#### DASHBOARD / STATISTICS / BUSSINESS

- BUSSINESS RATING
- MOST LISTED PRODUCTS
- TOP RATED PRODUCTS
- LESS RATED PRODUCT

#### DASHBOARD / STATISTICS / USERS

- NEAREST DISCOUNTS
- TOP RATED PRODUCT IN CITY
- TOP RATED BUSSINESS IN CITY

#### DASHBOARD / ADMIN

- APPROVE OR DISCARD BUSSINESS
- APPROVE, DISCARD OR CREATE TAGS
- APPROVE, DISCARD OR CREATE BRANDS
- APPROVE, DISCARD OR CREATE PRODUCTS

#### MAILER

- RECOVER PASSWORD
- BUSSINESS APPROVED, REJECTED
- PRODUCTS APPROVED, REJECTED, MODIFIED, EXISTENT
- BRAND APPROVED, REJECTED, MODIFIED, EXISTENT

# NEED TO

- MULTIPLE FILES FOR A SINGLE BACKEND X
- INTEGRATE BOOTSTRAP WITHIN THE TEMPLATES
- BUILD MAILER
- BUILD AUTH X
- STORE FILE ON SV VS STORE FILE ON DB
- THINK HOW IMPLEMENT DISTANCE RELATION X
- ROLE ASIGNAMENT BY TUPLE X
- PROTECT ROUTES
- GENERATE SLUGS
- RELATE TABLES ON CREATION AND UPDATE X
- ADD LIMITS TO CITY ON FINDINGS --
- ASSING DATA MODEL X
- RATING AVERAGE
-

# INTERMEDIATE TABLES

- tag <> bussiness
- tag <> product
- image <> bussiness
- image <> brand
- document <> bussiness
- document <> user(owner)
- list <> stock

VIEWS

### BASIC

    ## DASHBOARD
    	- Popular Products on City X
    	- Popular Bussiness on City X
    	- Nearest Bussiness X
    	- Most Discounts Bussiness on City X
    	- Recent Added Products X

    ## SEARCH
    	* Pagination
    	* Products and Bussiness
    	* Tagging
    	* Filter by popular, cheap

    ## PRODUCTS DETAIL
    	- Bussiness which have that product X
    		* At which price
    		* At which distance
    	- Brand basic info X
    	- Load Images

    ## BUSSINESS DETAILS
    	* Distance
    	- Popular Products of that bussiness X
    	- Popular Brands of that bussiness X
    	- Top discounts of that bussiness X


    ## BRAND DETAILS
    	- Popular Products by Brand X
    	- Popular Bussiness with that brand X

    ## OWNER DETAILS
    	- Popular Products of that owner X
    	- Popular Bussiness of that owner X

### CLIENT

    * Become Owner
    ## PROFILE INFO
    	- Edit mail
    	- Change password
    	- Change Basic Info

    ## LIST
    	- Drop item

### OWNER

    * CRUD For Product
    * CRUD For Brand
    * CRUD For Bussiness
    * CRUD For Stock

    ## DASHBOARD
    	- Popular Products of that bussiness X
    	- Popular Brands of that bussiness X
    	- Less popular Products X (try polymorph)

    ## BUSSINESS
    	- All Bussiness of the owner X


    ## STOCKS

    ## PROFILE
    	* Redirect to Create Bussiness

### ADMIN

    ## BUSSINESS
    	- Popular Bussiness X
    	- New Products X
    	- Get Tags (distribute them on controller)

    ## MANAGE MENU
    	# BUSSINESS
    	# TAGS
    	# PRODUCTS
    	# BRANDS

### MISC
