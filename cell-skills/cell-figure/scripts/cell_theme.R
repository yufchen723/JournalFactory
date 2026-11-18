# Cell (Cell Press) figure style for ggplot2 / patchwork.
#
# Numbers: cell-shared/journal-formats/cell.md section 5 (read on cell.com 2026-11-18):
# widths 85 / 114 / 174 mm, Arial only, text about 6-8 pt, capital panel letters,
# strokes 0.5-1.5 pt, RGB, no red with green, TIFF or PDF, <= 20 MB per figure.
# Choices Cell does not make (panel-letter size and weight, palette) are marked HOUSE.
#
#   source("cell_theme.R")
#   p <- (p1 | p2) / p3 + cell_tags()
#   save_cell_r(p, "Figure 1", width = "full", height_mm = 110)

CELL <- list(
  widths_mm = c(single = 85, mid = 114, full = 174),
  recommended_max_mm = c(165, 200),
  text_pt = c(6, 8),
  stroke_pt = c(0.5, 1.5),
  dpi = c(colour = 300, grayscale = 300, bw = 500, lineart = 1000),
  max_file_mb = 20
)

# ggplot2 linewidth is in mm of a 96-dpi-era unit: 1 linewidth = 72.27 / 25.4 / (72.27/96)... in
# practice 1 pt = 1 / 2.13 linewidth units. Use pt() for every line so strokes are true points.
pt <- function(x) x / 2.13

# HOUSE palette: colour-blind safe; red (vermilion) and green are never both in the default set.
cell_palette <- c(blue = "#0072B2", orange = "#E69F00", sky = "#56B4E9", vermilion = "#D55E00",
                  purple = "#CC79A7", yellow = "#F0E442", gray = "#7F7F7F")
cell_cols <- function(n = length(cell_palette)) {
  if (n > length(cell_palette)) stop("more groups than palette colours: merge groups or use facets")
  unname(cell_palette[seq_len(n)])
}

cell_font <- function() {
  fam <- "Arial"
  ok <- tryCatch({
    if (requireNamespace("systemfonts", quietly = TRUE)) {
      grepl("arial", basename(systemfonts::match_fonts("Arial")$path), ignore.case = TRUE)
    } else TRUE
  }, error = function(e) TRUE)
  if (!isTRUE(ok)) {
    warning("Arial is not installed; a substitute will be drawn. Cell asks for Arial only: ",
            "re-export on a machine with Arial before the production upload.", call. = FALSE)
  }
  fam
}

theme_cell <- function(base_size = 7, tick_size = 6, family = "Arial") {
  stopifnot(base_size >= CELL$text_pt[1], base_size <= CELL$text_pt[2], tick_size >= CELL$text_pt[1])
  ggplot2::theme_classic(base_size = base_size, base_family = family) +
    ggplot2::theme(
      line = ggplot2::element_line(linewidth = pt(0.5), colour = "black"),
      rect = ggplot2::element_rect(linewidth = pt(0.5)),
      text = ggplot2::element_text(colour = "black", size = base_size),
      legend.key = ggplot2::element_blank(),
      panel.background = ggplot2::element_blank(),
      plot.background = ggplot2::element_rect(fill = "white", colour = NA),
      axis.title = ggplot2::element_text(size = base_size),
      axis.text = ggplot2::element_text(size = tick_size, colour = "black"),
      axis.line = ggplot2::element_line(linewidth = pt(0.5), colour = "black"),
      axis.ticks = ggplot2::element_line(linewidth = pt(0.5), colour = "black"),
      axis.ticks.length = grid::unit(2.5, "pt"),
      legend.title = ggplot2::element_text(size = tick_size),
      legend.text = ggplot2::element_text(size = tick_size),
      legend.key.size = grid::unit(8, "pt"),
      legend.background = ggplot2::element_blank(),
      legend.margin = ggplot2::margin(0, 0, 0, 0),
      strip.text = ggplot2::element_text(size = base_size),
      strip.background = ggplot2::element_blank(),
      plot.title = ggplot2::element_text(size = base_size, face = "plain", hjust = 0),
      plot.tag = ggplot2::element_text(size = 8, face = "bold"),      # HOUSE: bold 8 pt; capitals are the Cell rule
      plot.tag.position = c(0, 1),
      panel.grid = ggplot2::element_blank(),
      plot.margin = ggplot2::margin(3, 3, 3, 3)
    )
}

# Capital panel letters for a patchwork: p + cell_tags()
cell_tags <- function() patchwork::plot_annotation(tag_levels = "A")

scale_colour_cell <- function(...) ggplot2::scale_colour_manual(values = unname(cell_palette), ...)
scale_fill_cell <- function(...) ggplot2::scale_fill_manual(values = unname(cell_palette), ...)
# Continuous: viridis (sequential) or blue-white-red centred at 0 (diverging). Never rainbow, never red-green.
scale_fill_cell_seq <- function(...) ggplot2::scale_fill_viridis_c(...)
scale_fill_cell_div <- function(..., midpoint = 0) {
  ggplot2::scale_fill_gradient2(low = "#2166AC", mid = "white", high = "#B2182B", midpoint = midpoint, ...)
}

# Colour bar with 0.5 pt ticks (the ggplot default ticks are thinner than Cell's minimum).
guide_colourbar_cell <- function(...) {
  ggplot2::guide_colourbar(ticks.linewidth = pt(0.5), ticks.colour = "black", frame.colour = NA,
                           barwidth = grid::unit(6, "pt"), barheight = grid::unit(40, "pt"), ...)
}

cell_width_mm <- function(width) {
  if (is.character(width)) return(unname(CELL$widths_mm[[width]]))
  if (width > CELL$widths_mm[["full"]]) stop("wider than Cell's full page width (174 mm)")
  width
}

# Gray fills that follow Cell's rule (10-80% black, at least 20% apart): at most 4.
cell_grays <- function(n) {
  if (n > 4) stop("Cell's gray rule allows at most 4 distinguishable gray fills")
  if (n == 1) return(grDevices::gray(0.55))
  grDevices::gray(1 - seq(0.10, 0.80, length.out = n))
}

.cell_script_dir <- local({
  d <- tryCatch(dirname(normalizePath(sys.frame(1)$ofile)), error = function(e) NULL)
  function() d
})

# Write PDF (vector, fonts embedded) and LZW TIFF at the exact size, then audit both files.
save_cell_r <- function(plot, stem, width = "full", height_mm = 100, kind = "colour", dpi = NULL,
                        formats = c("pdf", "tiff"), family = cell_font(), audit = TRUE) {
  w <- cell_width_mm(width) / 25.4
  h <- height_mm / 25.4
  if (height_mm > CELL$recommended_max_mm[2]) {
    warning("height above Cell's recommended 200 mm; the legend may not fit under the figure", call. = FALSE)
  }
  need <- CELL$dpi[[kind]]
  dpi <- if (is.null(dpi)) need else dpi
  if (dpi < need) stop(sprintf("%s figures need at least %d dpi", kind, need))
  files <- character(0)
  if ("pdf" %in% formats) {
    f <- paste0(stem, ".pdf")
    if (capabilities("cairo")) grDevices::cairo_pdf(f, width = w, height = h, family = family)
    else grDevices::pdf(f, width = w, height = h, family = "Helvetica", useDingbats = FALSE)
    print(plot); grDevices::dev.off(); files <- c(files, f)
  }
  if ("tiff" %in% formats) {
    f <- paste0(stem, ".tiff")
    if (requireNamespace("ragg", quietly = TRUE)) {
      ragg::agg_tiff(f, width = w, height = h, units = "in", res = dpi, compression = "lzw", background = "white")
    } else {
      grDevices::tiff(f, width = w, height = h, units = "in", res = dpi, compression = "lzw", bg = "white",
                      type = if (capabilities("cairo")) "cairo" else getOption("bitmapType"))
    }
    print(plot); grDevices::dev.off(); files <- c(files, f)
  }
  if ("png" %in% formats) {
    f <- paste0(stem, ".png")
    grDevices::png(f, width = w, height = h, units = "in", res = dpi, bg = "white",
                   type = if (capabilities("cairo")) "cairo" else getOption("bitmapType"))
    print(plot); grDevices::dev.off(); files <- c(files, f)
  }
  mb <- file.size(files) / 1e6
  if (any(mb > CELL$max_file_mb)) warning("a file is above Cell's 20 MB limit: ", paste(files[mb > CELL$max_file_mb], collapse = ", "))
  if (audit) {
    v <- file.path(if (is.null(.cell_script_dir())) "." else .cell_script_dir(), "validate_cell_figure.py")
    if (file.exists(v) && nzchar(Sys.which("python3"))) {
      # The audit reads the exported files; it does not draw anything.
      system2("python3", c(shQuote(v), shQuote(files), "--kind", kind, "--json", shQuote(paste0(stem, ".audit.json"))))
    } else {
      message("validate_cell_figure.py not found next to cell_theme.R; run it on: ", paste(files, collapse = ", "))
    }
  }
  invisible(files)
}
