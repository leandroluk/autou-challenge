"use client"

import { Tabs as TabsPrimitive } from "@base-ui/react/tabs"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/components/utils"

export function Tabs({
  className,
  orientation = "horizontal",
  ...props
}: TabsPrimitive.Root.Props) {
  return (
    <TabsPrimitive.Root
      data-slot="tabs"
      data-orientation={orientation}
      className={cn(
        "gap-2 group/tabs flex data-horizontal:flex-col",
        className
      )}
      {...props}
    />
  )
}

export const tabsListVariants = cva(`
  rounded-lg p-[3px] group-data-horizontal/tabs:h-8 data-[variant=line]:rounded-none
  w-fit items-center justify-center text-muted-foreground group-data-vertical/tabs:h-fit
  group-data-vertical/tabs:flex-col group/tabs-list inline-flex`, {
  variants: {
    variant: {
      default: "bg-muted",
      line: "gap-1 bg-transparent",
    },
  },
  defaultVariants: {
    variant: "default",
  },
})

export function TabsList({
  className,
  variant = "default",
  ...props
}: TabsPrimitive.List.Props & VariantProps<typeof tabsListVariants>) {
  return (
    <TabsPrimitive.List
      data-slot="tabs-list"
      data-variant={variant}
      className={cn(tabsListVariants({ variant }), className)}
      {...props}
    />
  )
}

export function TabsTrigger({
  className,
  ...props
}: TabsPrimitive.Tab.Props) {
  return (
    <TabsPrimitive.Tab
      data-slot="tabs-trigger"
      className={cn(`
        group-data-[variant=default]/tabs-list:data-active:shadow-sm gap-1.5 [&_svg:not([class*='size-'])]:size-4
        group-data-[variant=line]/tabs-list:data-active:shadow-none group-data-vertical/tabs:after:w-0.5 relative
        items-center justify-center whitespace-nowrap font-medium text-foreground/60 transition-all border-transparent
        group-data-vertical/tabs:w-full group-data-vertical/tabs:justify-start py-0.5 focus-visible:ring-ring/50
        hover:text-foreground focus-visible:border-ring focus-visible:ring-[3px] rounded-md border [&_svg]:shrink-0
        focus-visible:outline-1 focus-visible:outline-ring disabled:pointer-events-none disabled:opacity-50 px-1.5
        aria-disabled:pointer-events-none aria-disabled:opacity-50 dark:text-muted-foreground after:opacity-0 text-sm
        dark:hover:text-foreground [&_svg]:pointer-events-none data-active:text-foreground after:transition-opacity
        group-data-[variant=line]/tabs-list:bg-transparent data-active:bg-background dark:data-active:border-input
        group-data-[variant=line]/tabs-list:data-active:bg-transparent after:absolute after:bg-foreground inline-flex
        dark:group-data-[variant=line]/tabs-list:data-active:border-transparent group-data-horizontal/tabs:after:h-0.5
        dark:group-data-[variant=line]/tabs-list:data-active:bg-transparent group-data-vertical/tabs:after:inset-y-0
        dark:data-active:bg-input/30 dark:data-active:text-foreground group-data-horizontal/tabs:after:-bottom-1.25
        group-data-horizontal/tabs:after:inset-x-0 group-data-vertical/tabs:after:-right-1 h-[calc(100%-1px)] flex-1
        group-data-[variant=line]/tabs-list:data-active:after:opacity-100`, className)}
      {...props}
    />
  )
}

export function TabsContent({
  className,
  ...props
}: TabsPrimitive.Panel.Props) {
  return (
    <TabsPrimitive.Panel
      data-slot="tabs-content"
      className={cn("text-sm flex-1 outline-none", className)}
      {...props}
    />
  )
}
