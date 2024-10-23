use std::{iter::Map, ops::Range};

use image::DynamicImage;
use pdf2image::{
    image::ImageFormat, PDF2ImageError, RenderOptions, RenderOptionsBuilder, DPI, PDF,
};
use prgrs::Prgrs;

fn main() -> Result<(), PDF2ImageError> {
    let pdf = PDF::from_file("纯粹理性批判 (〔德〕康德著；邓晓芒译) (Z-Library).pdf").unwrap();
    let page_batches = batch_render(&pdf);

    let mut idx = 0;
    for page_batch in page_batches {
        let pages = page_batch?;
        for page in pages {
            let s = format!("kant_ims/page_{idx:0>3}.png");
            page.save_with_format(s, ImageFormat::Png)?;
            idx += 1;
        }
    }
    Ok(())
}
///
/// Rendering all at once causes memory overflow.
/// 
fn batch_render<'a>(
    pdf: &'a PDF,
) -> Map<Prgrs<Range<u32>>, impl FnMut(u32) -> Result<Vec<DynamicImage>, PDF2ImageError> + 'a> {
    let page_count = pdf.page_count();

    let batch_size = 20;
    let batch_count = (page_count + batch_size - 1) / batch_size;

    let batch_pages = Prgrs::new(0..batch_count, batch_count as usize).map(move |idx| {
        let render_options = RenderOptions {
            resolution: DPI::Uniform(600),
            ..RenderOptionsBuilder::default().build()?
        };
        let start = idx * batch_size + 1;
        let end = std::cmp::min(start + batch_size, page_count);
        pdf.render(pdf2image::Pages::Range(start..=end), render_options)
    });

    batch_pages
}
