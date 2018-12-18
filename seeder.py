from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, CategoryItem

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# delete all bast record
session.query(CategoryItem).filter(id != 0).delete()
session.commit()

# categories

category1 = Category(name="Business")

session.add(category1)
session.commit()

category2 = Category(name="Science")

session.add(category2)
session.commit()

category3 = Category(name="Fiction")

session.add(category3)
session.commit()

category4 = Category(name="Philosophy")

session.add(category4)
session.commit()

category5 = Category(name="Biography")

session.add(category5)
session.commit()


# Category Items


# Items For Category 1 "Business"

item1 = CategoryItem(user_id=1, categoryId=1, title="The 7 Habits of Highly Effective People", author="Stephen R. Covey", picture="/photo/1.jpg",
                     description="What are the habits of successful people? The 7 Habits of Highly Effective People has captivated readers for 25 years. It has transformed the lives of Presidents and CEOs, educators, parents, and students — in short, millions of people of all ages and occupations have benefited from Dr. Covey's 7 Habits book. And, it can transform you. Infographics Edition: Stephen Covey’s cherished classic commemorates the timeless wisdom and power of the 7 Habits book, and does it in a highly readable and understandable, infographics format.")

session.add(item1)
session.commit()

item2 = CategoryItem(user_id=1, categoryId=1, title="Dare to Lead", author="Brené Brown", picture="/photo/2.jpg",
                     description="Brené Brown has taught us what it means to dare greatly, rise strong, and brave the wilderness. Now, based on new research conducted with leaders, change makers, and culture shifters, she's showing us how to put those ideas into practice so we can step up and lead. Leadership is not about titles, status, and power over people. Leaders are people who hold themselves accountable for recognizing the potential in people and ideas and developing that potential. This is a book for everyone who is ready to choose courage over comfort, make a difference, and lead.  When we dare to lead, we don't pretend to have the right answers; we stay curious and ask the right questions. We don't see power as finite and hoard it; we know that power becomes infinite when we share it and work to align authority and accountability. We don't avoid difficult conversations and situations; we lean into the vulnerability that's necessary to do good work. ")

session.add(item2)
session.commit()

item3 = CategoryItem(user_id=1, categoryId=1, title="Leadership: In Turbulent Times", author="Doris Kearns Goodwin", picture="/photo/3.jpg",
                     description=''' “After five decades of magisterial output, Doris Kearns Goodwin leads the league of presidential historians. Insight is her imprint.”—USA TODAY

“A book like Leadership should help us raise our expectations of our national leaders, our country and ourselves.”—The Washington Post

“We can only hope that a few of Goodwin’s many readers will find in her subjects’ examples a margin of inspiration and a resolve to steer the country to a better place.”—The New York Times Book Review

In this culmination of five decades of acclaimed studies in presidential history, Pulitzer Prize-winning author Doris Kearns Goodwin offers an illuminating exploration of the early development, growth, and exercise of leadership. ''')

session.add(item3)
session.commit()

item4 = CategoryItem(user_id=1, categoryId=1, title="The Fifth Risk", author="Michael Lewis ", picture="/photo/4.jpg",
                     description='''What are the consequences if the people given control over our government have no idea how it works?

"The election happened," remembers Elizabeth Sherwood-Randall, then deputy secretary of the Department of Energy. "And then there was radio silence." Across all departments, similar stories were playing out: Trump appointees were few and far between; those that did show up were shockingly uninformed about the functions of their new workplace. Some even threw away the briefing books that had been prepared for them.''')

session.add(item4)
session.commit()

item5 = CategoryItem(user_id=1, categoryId=1, title="Bad Blood: Secrets and Lies in a Silicon Valley Startup", author="John Carreyrou ", picture="/photo/5.jpg",
                     description='''In 2014, Theranos founder and CEO Elizabeth Holmes was widely seen as the female Steve Jobs: a brilliant Stanford dropout whose startup "unicorn" promised to revolutionize the medical industry with a machine that would make blood testing significantly faster and easier. Backed by investors such as Larry Ellison and Tim Draper, Theranos sold shares in a fundraising round that valued the company at more than $9 billion, putting Holmes's worth at an estimated $4.7 billion. There was just one problem: The technology didn't work. ''')

session.add(item5)
session.commit()


# Items For Category 2 "Science"

item1 = CategoryItem(user_id=1, categoryId=2, title="What If?", author="Randall Munroe", picture="/photo/6.jpg",
                     description='''Millions of people visit xkcd.com each week to read Randall Munroe’s iconic webcomic. His stick-figure drawings about science, technology, language, and love have a large and passionate following.

Fans of xkcd ask Munroe a lot of strange questions. What if you tried to hit a baseball pitched at 90 percent the speed of light? How fast can you hit a speed bump while driving and live? If there was a robot apocalypse, how long would humanity last?''')

session.add(item1)
session.commit()


item2 = CategoryItem(user_id=2, categoryId=2, title="Sapiens: A Brief History of Humankind", author="Yuval Noah Harari ", picture="/photo/7.jpg",
                     description='''From a renowned historian comes a groundbreaking narrative of humanity’s creation and evolution—a #1 international bestseller—that explores the ways in which biology and history have defined us and enhanced our understanding of what it means to be “human.”

One hundred thousand years ago, at least six different species of humans inhabited Earth. Yet today there is only one—homo sapiens. What happened to the others? And what may happen to us?''')

session.add(item2)
session.commit()

item3 = CategoryItem(user_id=1, categoryId=2, title="There's No Place Like Space", author="Tish Rabe", picture="/photo/8.jpg",
                     description='''Au revoir, Pluto! In this newly revised, bestselling backlist title, beginning readers and budding astronomers are launched on a wild trip to visit the now eight planets in our solar system (per the International Astronomical Union’s 2006 decision to downgrade Pluto from a planet to a dwarf planet), along with the Cat in the Hat, Thing One, Thing Two, Dick, and Sally. It’s a reading adventure that’s out of this world!''')
session.add(item3)
session.commit()

item4 = CategoryItem(user_id=2, categoryId=2, title="Women in Science", author="Rachel Ignotofsky", picture="/photo/9.jpg",
                     description='''A charmingly illustrated and educational book, New York Times best seller Women in Science highlights the contributions of fifty notable women to the fields of science, technology, engineering, and mathematics (STEM) from the ancient to the modern world. Full of striking, singular art, this fascinating collection also contains infographics about relevant topics such as lab equipment, rates of women currently working in STEM fields, and an illustrated scientific glossary. The trailblazing women profiled include well-known figures like primatologist Jane Goodall, as well as lesser-known pioneers such as Katherine Johnson, the African-American physicist and mathematician who calculated the trajectory of the 1969 Apollo 11 mission to the moon. ''')

session.add(item4)
session.commit()

item5 = CategoryItem(user_id=1, categoryId=2, title="Atomic Habits", author="James Clear", picture="/photo/10.jpg",
                     description='''No matter your goals, Atomic Habits offers a proven framework for improving--every day. James Clear, one of the world's leading experts on habit formation, reveals practical strategies that will teach you exactly how to form good habits, break bad ones, and master the tiny behaviors that lead to remarkable results.

If you're having trouble changing your habits, the problem isn't you. The problem is your system. Bad habits repeat themselves again and again not because you don't want to change, but because you have the wrong system for change. You do not rise to the level of your goals. You fall to the level of your systems. Here, you'll get a proven system that can take you to new heights.''')

session.add(item5)
session.commit()

# Items For Category 3 "Fiction"

item1 = CategoryItem(user_id=2, categoryId=3, title="Beneath a Scarlet Sky: A Novel", author="Mark Sullivan", picture="/photo/11.jpg",
                     description='''Pino Lella wants nothing to do with the war or the Nazis. He’s a normal Italian teenager—obsessed with music, food, and girls—but his days of innocence are numbered. When his family home in Milan is destroyed by Allied bombs, Pino joins an underground railroad helping Jews escape over the Alps, and falls for Anna, a beautiful widow six years his senior.''')

session.add(item1)
session.commit()

item2 = CategoryItem(user_id=1, categoryId=3, title="The Hideaway", author="Lauren K. Denton", picture="/photo/12.jpg",
                     description='''After her last remaining family member dies, Sara Jenkins goes home to The Hideaway, her grandmother Mags’s ramshackle B&B in Sweet Bay, Alabama. She intends to quickly tie up loose ends then return to her busy life and thriving antique shop in New Orleans. Instead, she learns Mags has willed The Hideaway to her and charged her with renovating it—no small task considering her grandmother’s best friends, a motley crew of senior citizens, still live there.''')

session.add(item2)
session.commit()

item3 = CategoryItem(user_id=2, categoryId=3, title="The Boy in the Striped Pajamas", author="John Boyne", picture="/photo/13.jpg",
                     description='''Berlin, 1942: When Bruno returns home from school one day, he discovers that his belongings are being packed in crates. His father has received a promotion and the family must move to a new house far, far away, where there is no one to play with and nothing to do. A tall fence stretches as far as the eye can see and cuts him off from the strange people in the distance.''')

session.add(item3)
session.commit()

item4 = CategoryItem(user_id=1, categoryId=3, title="All the Ugly and Wonderful Things", author="Bryn Greenwood", picture="/photo/14.jpg",
                     description='''A beautiful and provocative love story between two unlikely people and the hard-won relationship that elevates them above the Midwestern meth lab backdrop of their lives.

As the daughter of a drug dealer, Wavy knows not to trust people, not even her own parents. It's safer to keep her mouth shut and stay out of sight. Struggling to raise her little brother, Donal, eight-year-old Wavy is the only responsible adult around. Obsessed with the constellations, she finds peace in the starry night sky above the fields behind her house, until one night her star gazing causes an accident. After witnessing his motorcycle wreck, she forms an unusual friendship with one of her father's thugs, Kellen, a tattooed ex-con with a heart of gold.''')

session.add(item4)
session.commit()

item5 = CategoryItem(user_id=1, categoryId=3, title="The Great Alone", author="Kristin Hannah", picture="/photo/15.jpg",
                     description='''Alaska, 1974. Ernt Allbright came home from the Vietnam War a changed and volatile man. When he loses yet another job, he makes the impulsive decision to move his wife and daughter north where they will live off the grid in America’s last true frontier.

Cora will do anything for the man she loves, even if means following him into the unknown. Thirteen-year-old Leni, caught in the riptide of her parents’ passionate, stormy relationship, has little choice but to go along, daring to hope this new land promises her family a better future.''')

session.add(item5)
session.commit()

# Items For Category 4 "Philosophy"

item1 = CategoryItem(user_id=2, categoryId=4, title="Plato and a Platypus Walk into a Bar . . .", author="Thomas Cathcart ", picture="/photo/16.jpg",
                     description='''Outrageously funny, Plato and a Platypus Walk into a Bar... has been a breakout bestseller ever since authors—and born vaudevillians—Thomas Cathcart and Daniel Klein did their schtick on NPR’s Weekend Edition. Lively, original, and powerfully informative, Plato and a Platypus Walk Into a Bar... is a not-so-reverent crash course through the great philosophical thinkers and traditions, from Existentialism (What do Hegel and Bette Midler have in common?) to Logic (Sherlock Holmes never deduced anything). Philosophy 101 for those who like to take the heavy stuff lightly, this is a joy to read—and finally, it all makes sense!''')

session.add(item1)
session.commit()


item2 = CategoryItem(user_id=1, categoryId=4, title="101 Questions for Humanity", author="J Edward Neill", picture="/photo/17.jpg",
                     description='''101 Questions for Humanity - The supreme coffee table book for armchair philosophers. Designed to provoke, question, and challenge. Crack the cover open during big parties, small gatherings, or lonely nights on the couch. Once you taste one question, you'll want to devour them all.''')

session.add(item2)
session.commit()


item3 = CategoryItem(user_id=2, categoryId=4, title="The Philosophy Book", author="DK", picture="/photo/18.jpg",
                     description='''Explore the history and concepts of philosophy, from the big thinkers to complex theories, with straightforward text and witty illustrations that demystify an often daunting subject matter. Now in paperback.

Are the ideas of René Descartes, Mary Wollstonecraft, John Locke, and Thomas Hobbes still relevant today? The Philosophy Book unpacks the writings and ideas of more than 100 of history's well-known philosophers, taking you on a journey from ancient Greece to modern day. Explore feminism, rationalism, idealism, existentialism, and other influential movements in the world of philosophy.''')

session.add(item3)
session.commit()


item4 = CategoryItem(user_id=1, categoryId=4, title="The Book of Joy", author="Dalai Lama", picture="/photo/19.jpg",
                     description='''Nobel Peace Prize Laureates His Holiness the Dalai Lama and Archbishop Desmond Tutu have survived more than fifty years of exile and the soul-crushing violence of oppression. Despite their hardships—or, as they would say, because of them—they are two of the most joyful people on the planet.

In April 2015, Archbishop Tutu traveled to the Dalai Lama's home in Dharamsala, India, to celebrate His Holiness's eightieth birthday and to create what they hoped would be a gift for others. They looked back on their long lives to answer a single burning question: How do we find joy in the face of life's inevitable suffering?''')

session.add(item4)
session.commit()


item5 = CategoryItem(user_id=1, categoryId=4, title="Philosophy 101", author="Paul Kleinman", picture="/photo/20.jpg",
                     description='''Too often, textbooks turn the noteworthy theories, principles, and figures of philosophy into tedious discourse that even Plato would reject. Philosophy 101 cuts out the boring details and exhausting philosophical methodology, and instead, gives you a lesson in philosophy that keeps you engaged as you explore the fascinating history of human thought and inquisition.

From Aristotle and Heidegger to free will and metaphysics, Philosophy 101 is packed with hundreds of entertaining philosophical tidbits, illustrations, and thought puzzles that you won't be able to find anywhere else.''')

session.add(item5)
session.commit()


# Items For Category 5 "Biography"

item1 = CategoryItem(user_id=1, categoryId=5, title="Obama: 101 Best Covers:", author="Ben Arogundade ", picture="/photo/21.jpg",
                     description='''OBAMA & NEW YORK TIMES 
Featured titles within this definitive collection include Time, Newsweek, Rolling Stone, Vogue, Vanity Fair, The New Yorker, Esquire, Ebony, Essence, Vibe, The Guardian and The New York Times, amongst others. Many of the covers featuring the 44th US president were flattering. Obama never looked better than when he featured on the front of The New York Times or Rolling Stone. (See pages 40 and 69 of the Obama book).''')

session.add(item1)
session.commit()


item2 = CategoryItem(user_id=2, categoryId=5, title="Hindsight", author="Justin Timberlake ", picture="/photo/22.jpg",
                     description='''"I can't help that my music shows who I am in this moment, what I'm drawn to, what I'm wondering about. I don't want to help it. What you hear in the words, what you feel in those songs—that's what I was feeling when I wrote them. I want you to see me, just like I want to see you."

— Justin Timberlake''')

session.add(item2)
session.commit()


item3 = CategoryItem(user_id=2, categoryId=5, title="Let's Go (So We Can Get Back)", author="Jeff Tweedy", picture="/photo/23.jpg",
                     description='''Few bands have inspired as much devotion as the Chicago rock band Wilco, and it's thanks, in large part, to the band's singer, songwriter, and guiding light: Jeff Tweedy. But while his songs and music have been endlessly discussed and analyzed, Jeff has rarely talked so directly about himself, his life, and his artistic process''')

session.add(item3)
session.commit()


item4 = CategoryItem(user_id=2, categoryId=5, title="Kant", author="Manfred Kuehn ", picture="/photo/24.jpg",
                     description='''This is the first full-length biography in more than fifty years of Immanuel Kant, one of the giants among the pantheon of Western philosophers, and one of the most powerful and influential in contemporary philosophy. Taking account of the most recent scholarship, Manfred Kuehn allows the reader to follow the same journey that Kant himself took in emerging as a central figure in modern philosophy. Manfred Kuehn was formerly Professor of Philosophy at Purdue University. A specialist on German philosophy of the period, he is the author of numerous articles and papers on Immanuel Kant.''')

session.add(item4)
session.commit()


item5 = CategoryItem(user_id=1, categoryId=5, title="J.R.R. Tolkien: A Life Inspired", author="Wyatt North ", picture="/photo/25.jpg",
                     description='''John Ronald Reuel Tolkien was Professor of Anglo-Saxon (Old English) at the University of Oxford. His research on Beowulf is still considered a standard in the field. Tolkien, however, unlike most Oxford dons, stepped out of his role as professor to create popular literature. Tolkien’s best-known writings were The Hobbit and The Lord of the Rings, in which he created a fully realized world known as Middle-earth, vaguely identifiable as Northern Europe in a pre-history that never was. To bring his world to life, he produced detailed geography and cartography as well as a legendary background. He peopled the world with diverse types of inhabitants and created spoken and written languages for them. By doing this, he essentially created modern fantasy literature and a standard for subsequent writers to chase and miss. A British poll at the end of the twentieth century named The Lord of the Rings the most important English-language work of that century. During his lifetime, Tolkien did not appreciate people focusing on him rather than on his writings. He felt that his writings were more worthy of attention. With apologies to the late gentleman, he is now due some notice.''')

session.add(item5)
session.commit()


print("added catalog items!")
