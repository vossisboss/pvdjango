# Next Steps

Now you have a working foundation for a multilingual website. You don't have _all_ the pieces though. So what could you try next? Here are some ideas:

### Add your favorite frontend

Wagtail was created to provide a backend framework that works well with as many frontend technologies as possible. Whether you prefer something simple like [Bootstrap](https://getbootstrap.com/) or something more complex like [React](https://reactjs.org/) or [Next.js](https://nextjs.org/), you can try pretty much everything with Wagtail. If you need some inspiration, Kalob Taulien did a good video on [Bootstrap](https://learnwagtail.com/tutorials/adding-bootstrap-4-theme-to-our-wagtail-website/) and Michael Yin has a good package for a [frontend setup using Webpack](https://github.com/AccordBox/python-webpack-boilerplate) that works well with Django.

### Level up your SEO

Marketing people have high expectations, and the default options in Wagtail don't typically satisfy them. So try adding one of the packages that expands your SEO options in Wagtail. The two most popular packages that are available include:

[wagtail-metadata](https://github.com/neon-jungle/wagtail-metadata)
[wagtail-seo](https://github.com/coderedcorp/wagtail-seo)

### Experiment with adding different elements from the Wagtail Bakery Demo

The [Wagtail Bakery Demo](https://github.com/wagtail/bakerydemo) is an example project that can provide you with some code examples to borrow for your own project. Have a look at it and see if there are any bits you like and want to try out. The navigation menu you created for this tutorial is pretty basic. The template tag created for the main navigation in the [bakery demo](https://github.com/wagtail/bakerydemo/blob/main/bakerydemo/base/templatetags/navigation_tags.py) might be one worth borrowing.

### Experiment with StreamField blocks

There is a whole list of [default blocks](https://docs.wagtail.org/en/stable/reference/streamfield/blocks.html) you can use in Wagtail. You can also combine these blocks in custom arrangements with [StructBlock](https://docs.wagtail.org/en/stable/topics/streamfield.html#structblock). If the default blocks are quite what you need, you can even add [custom blocks](https://docs.wagtail.org/en/stable/advanced_topics/customisation/streamfield_blocks.html#custom-streamfield-blocks) to your project. StreamField goes about as far as your imagination goes!

## Final words

Thank you for going through this tutorial with me! I hope you found it useful. If you have any questions, don't hesitate to reach out to me on [Twitter](https://twitter.com/meagenvoss) or through the [Wagtail Slack Community](https://wagtail.org/slack).