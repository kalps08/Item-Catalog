from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Category, Base, Item, User

# engine = create_engine('sqlite:///item-catalog.db')
engine = create_engine('postgresql://catalog:yourPassword@localhost/catalog')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/'
                     '18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Create dummy user
User2 = User(name="Justin Case", email="justinCase@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/'
                     '18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User2)
session.commit()

# Category #1 - Soccer
cat1 = Category(user_id=1, name="Soccer")
session.add(cat1)
session.commit()

# Items for Category #1 - Soccer
item1 = Item(user_id=1, title="New Balance Cleats",
             description="Full grain leather vamp combining durability and ball touch",
             category=cat1)
session.add(item1)
session.commit()

item2 = Item(user_id=1, title="Mercurial Lite Shin Guards",
             description="Never be distracted by guards slipping around "
                         "during a match. Security arrives in the Nike Mercurial "
                         "Lite SuperLock Shin Guards. These guards have a carved-away "
                         "foam backing that fine-tunes curvature thickness. SuperLock "
                         "attaches the shells to your sock fibers -- reducing layers as "
                         "it secures grip.",
             category=cat1)
session.add(item2)
session.commit()

item3 = Item(user_id=1, title="Adidas MLS Top Glider - Size 5",
             description="Featuring a butyl bladder that provides optimal air "
                         "retention and maintains its shape throughout the match, "
                         "the adidas 2017 MLS Top Glider Soccer Ball allows you to play "
                         "to your potential throughout the match. The outer shell is "
                         "comprised of machine-stitched panels.",
             category=cat1)
session.add(item3)
session.commit()

item4 = Item(user_id=1, title="Champion Soccer Coachs Clipboard",
             description="Champion Sports Soccer Dry Erase Coach Clipboard. "
                         "Easy wipe-off surface. 10in x 16in full field on one side. "
                         "Half field on reverse side. Complete with dry erase marker.",
             category=cat1)
session.add(item4)
session.commit()

# -------------------------------------------------------
# Category #2 - Basketball
cat1 = Category(user_id=1, name="Basketball")
session.add(cat1)
session.commit()

# Items for Category #2 - Basketball
item1 = Item(user_id=1, title="Spalding NBA Courtside Warriors Basketball",
             description="Standard size 7 basketball meaures 29 inches in "
                         "circumference, Made from durable rubber.",
             category=cat1)
session.add(item1)
session.commit()

item2 = Item(user_id=1, title="Under Armour Jet Mid Basketball Shoe",
             description="Feel great about your next big game because you have "
                         "the Under Armour Jet Mid basketball shoes to help you out! "
                         "This popular style has a leather and textile upper with a "
                         "padded tongue and collar to keep your ankles supported as you "
                         "sprint back and forth.",
             category=cat1)
session.add(item2)
session.commit()

item3 = Item(user_id=1, title="Majestic Golden State Warriors Primary Logo Tee",
             description="You'll be most stylish fan at the arena when you don this "
                         "Majestic Golden State Warriors Primary Logo T-Shirt. "
                         "The trendy Golden State Warriors graphics are perfect for "
                         "showing off your unique fashion sense.",
             category=cat1)
session.add(item3)
session.commit()

item4 = Item(user_id=1, title="Champion Basketball Coaching board",
             description="Double Sided Basketball Dry Erase Coaching Boards are perfect "
                         "for coaching and using under your scorebook as a hard surface. "
                         "These boards feature and easy wipe off surface.  "
                         "Full court on front and half court on back with a lineup box.  "
                         "Comes complete with dry erase marker.  Measures 10inw x 16inh.",
             category=cat1)
session.add(item4)
session.commit()

# -------------------------------------------------------
# Category #3 - Baseball

# Items for Category #3 - Baseball
item1 = Item(user_id=1, title="Easton Sports Ghost X -10",
             description="The latest composite design in a long line of legendary Easton "
                         "baseball bats is here for the 2018 season! Introducing the Ghost X, "
                         "a technical, powerful, and beautiful baseball bat that is "
                         "guaranteed to deliver a supernatural feel and speed unlike any other.",
             category=cat1)
session.add(item1)
session.commit()

item2 = Item(user_id=1, title="Rawlings Little League Game Baseball",
             description="This baseball has Rawlings superstitch raised seams with "
                         "full grain leather cover and composite cork and rubber center "
                         "which makes it perfect for Little League Baseball.",
             category=cat1)
session.add(item2)
session.commit()

item3 = Item(user_id=1, title="Tanners Team Sports Big Book Baseball Scorebook",
             description="Simple and straightforward, Generous Spiral binding and "
                         "Deluxe System-17 Baseball Scorebook ",
             category=cat1)
session.add(item3)
session.commit()

# -------------------------------------------------------
# Category #4 - Snowboarding
cat1 = Category(user_id=2, name="Snowboarding")
session.add(cat1)
session.commit()

# Items for Category #4 - Snowboarding
item1 = Item(user_id=2, title="Jones Snowboards Women's Dream Catcher",
             description="The Dream Catcher is our women's all-mountain board built "
                         "for riders looking for a high performance directional freeride "
                         "shape and a friendly flex. The Dream Catcher is stable, "
                         "confidence inspiring, yet soft enough to be playful in any terrain. "
                         "The Directional rocker profile and Spoon 1.0 base deliver epic "
                         "float in the fluff while the camber underfoot and Traction Tech "
                         "offer awesome edge grip when conditions firm up. The edges of the "
                         "Spoon nose are beveled up for improved turn fluidity while the "
                         "tail edges are beveled up for less catch. The Dream Catcher also "
                         "features an ECO-plastic topsheet for added ECO-performance.",
             category=cat1)
session.add(item1)
session.commit()

item2 = Item(user_id=2, title="Volcom Women's Shelter 3D Stretch Jacket",
             description="The Shelter 3D Stretch Insulated Jacket has 80g of insulation, "
                         "which is enough to keep you warm in single-digit temps. "
                         "And if you start to overheat on the uphill, just unzip the "
                         "arm vents to quickly cool down before you ride down.With a "
                         "15K waterproofing rating, it can keep you dry in almost every "
                         "type of conditions, even when you're hiking through the snow "
                         "rather than taking a lift.",
             category=cat1)
session.add(item2)
session.commit()

item3 = Item(user_id=2, title="Burton Custom Re:Flex",
             description="Returning once more to provide you with proven sleek and "
                         "smooth riding with complete control over the entire mountain, "
                         "the Burton Custom Snowboard Bindings and their soft, surfy flex "
                         "are incredibly easy to use for new and experienced riders alike. "
                         "Compatible with all major board mounting systems, the Custom's "
                         "Reactstraps form to your boot's shape and complement fully "
                         "adjustable hi-backs so you can dial in the perfect fit.",
             category=cat1)
session.add(item3)
session.commit()

item4 = Item(user_id=2, title="Smith Sport Optics Boy's Holt Jr. - Medium",
             description="If your little ripper disappears into the park every time "
                         "you ski together, get the Smith Kids Holt Jr. Helmet to "
                         "protect your grom's law school-worthy mind. The Bombshell "
                         "ABS hard shell and molded EPS foam liner are what you want "
                         "in between your kids noggin and a steel rail, and the skate-inspired "
                         "design is what the half-pint shredder wants to blend with friends. "
                         "The AirFlow Climate Control makes sure he wears this helmet on "
                         "the warmer days with rock-hard landings, and the AirEvac ventilation "
                         "reduces goggle fog by routing air from the forehead out the top vents. "
                         "The Holt Jr. doubles as a skate/bike helmet in the summer because of an "
                         "included convertible pad kit and the removable goggle clip.",
             category=cat1)
session.add(item4)
session.commit()

# -------------------------------------------------------
# Category #5 - Rock Climbing
cat1 = Category(user_id=1, name="Rock Climbing")
session.add(cat1)
session.commit()

# Items for Category #5 - Rock Climbing
item1 = Item(user_id=1, title="Black Diamond Camalot C4 #3",
             description="This Camalot generation isn't just lighter than the last "
                         "generation; it's also more convenient than any cam Black Diamond has ever made. "
                         "For starters, Black Diamond made the larger cams with stiffer stems and the smaller "
                         "cams with more flexible stems so they all have the same flex. The larger cams have "
                         "unique trigger keepers that lock the Camalots in a camming position to reduce racking "
                         "volume, and the keepers detach with a simple pull of the trigger when you're climbing. "
                         "Cams with the same color now come with bi-color slings for easier identification, "
                         "and the sling's tags are tucked underneath the shorter bar-tacks for a cleaner look. "
                         "Black Diamond also redesigned the tread pattern for a new look "
                         "to commemorate a brand new generation of Camalots.",
             category=cat1)
session.add(item1)
session.commit()

item2 = Item(user_id=1, title="Metolius Master Cam Size 2 Yellow",
             description="The Master Cam is a flexible, single-stem unit with an optimized cam angle "
                         "for increased holding power. The new Ultralight Master Cams are twenty "
                         "percent lighter than the originals. If you carry a double set of cams, the "
                         "weight savings is the same as a twelve ounce canned beverage of your choice. "
                         "When compared to other brands, the weight savings can be much more. "
                         "The new shark fin tooth pattern gives optimized bite in soft rock.",
             category=cat1)
session.add(item2)
session.commit()

# -------------------------------------------------------
# Category #6 - Swimming
cat1 = Category(user_id=1, name="Swimming")
session.add(cat1)
session.commit()

# Items for Category #6 - Swimming
item1 = Item(user_id=1, title="TYR Kids Happy Fish Swim Cap - Pink",
             description="Start your child's swim adventure off right with theKids' CharacTYR "
                         "Happy Fish Swim Cap. Designed specifically for growing athletes, "
                         "the LCSHFISH cap provides a snug, comfortable fit and protects hair "
                         "from damaging chlorine. This hypoallergenic, 100% silicone swim cap is "
                         "super durable, lightweight, anti-slip and easy to take on and off.",
             category=cat1)
session.add(item1)
session.commit()

item2 = Item(user_id=1, title="Alliance 30L Backpack Black/Pink",
             description="A new twist on an old classic, the LATBP30 is packed with state-of-the-art "
                         "features engineered for athletes on the go. With a cutting-edge space saving "
                         "design, the 30L maximizes storage without the bulk. In addition to contour "
                         "shaped padding for ideal ergonomics and lumbar comfort, the new design also "
                         "includes multiple front and side pockets, expandable mesh pockets for "
                         "separating wet and dry items, spring hooks for wet suits, a mesh water bottle "
                         "pocket, adjustable straps and a protective storage space for large electronics.",
             category=cat1)
session.add(item2)
session.commit()

item3 = Item(user_id=1, title="TYR Junior Blackhawk Racing Goggles",
             description="Engineered for both competition and training, the low profile design of "
                         "the Blackhawk Racing swimming goggle ensures a close fit with minimal drag. "
                         "Lightweight and streamlined, the Blackhawk’s watertight construction "
                         "includes Durafit Silicone gaskets, wide peripheral range and five removable "
                         "nosebridge size options.",
             category=cat1)
session.add(item3)
session.commit()

item4 = Item(user_id=1, title="FINIS Tempo Trainer Pro",
             description="The small, waterproof device easily secures beneath a swim cap and "
                         "transmits an audible tempo beep. Adjustable tempo offers the ability "
                         "to identify and maintain an ideal pace. Now with the option to replace the "
                         "battery, the Tempo Trainer Pro will last multiple lifetimes. Three different "
                         "training modes offer ultimate customization. The Tempo Trainer Pro includes a "
                         "clip for dryland exercise.",
             category=cat1)
session.add(item4)
session.commit()

item5 = Item(user_id=1, title="TYR USA Kick Board",
             description="The USA Classic Kickboard is the perfect tool for swim training and aquatic "
                         "exercise routines of all levels. Designed to build leg strength, this "
                         "training kick board immobilizes the arms and isolates the legs, so your body "
                         "works harder with every kick.",
             category=cat1)
session.add(item5)
session.commit()

# -------------------------------------------------------
# Category #7 - Biking

# Items for Category #7 - Biking
cat1 = Category(user_id=2, name="Biking")
session.add(cat1)
session.commit()

# Items for Category #7 - Biking
item1 = Item(user_id=2, title="Cannondale Bad Habit AL 2",
             description="The fun-loving nature of the Habit supersized with 27+ wheels to satisfy "
                         "those nagging dirt cravings - Frame: Bad Habit 27+, 120mm, Smartformed Alloy, "
                         "BB30, Flat Mount Brake, Pivoting Der Hanger, 1.5 Si headtube; Fork: Rockshox "
                         "Reba RL Boost, Tapered Steerer, 120mm, 15mm Through Axle, Poploc handlebar "
                         "mounted remote, 51mm offset ",
             category=cat1)
session.add(item1)
session.commit()

item2 = Item(user_id=2, title="Pearl Izumi Quest Short",
             description="A perennial favorite, our popular Quest Short defines value, fit, "
                         "durability and comfort at an entry level. - SELECT Transfer fabric sets "
                         "the benchmark for moisture transfer; Body: 88% nylon 12% spandex/ UPF 50+, "
                         "Weight: 250 g/m2, Imported",
             category=cat1)
session.add(item2)
session.commit()

item3 = Item(user_id=2, title="Scott Bikes Vivo Helmet",
             description="The Scott Vivo Helmet is the go to helmet for style conscious "
                         "trail riders. With the safety features such as extended coverage and "
                         "optimized geometry, and our top MRAS2 fit system, you can feel safe and "
                         "secure no matter where you ride.",
             category=cat1)
session.add(item3)
session.commit()


print("added menu items!")
